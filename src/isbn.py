import asyncio
import json
import re
import urllib.error
import urllib.parse
import urllib.request


GOOGLE_BOOKS_KEY = ""

def clean_isbn(raw: str) -> str | None:
    s = re.sub(r"[^0-9Xx]", "", raw or "").upper()
    return s if len(s) in (10, 13) else None


def to_isbn10(isbn13: str) -> str | None:
    if len(isbn13) != 13 or not isbn13.startswith("978") or not isbn13.isdigit():
        return None
    core = isbn13[3:12]
    total = sum((10 - i) * int(d) for i, d in enumerate(core))
    check = (11 - total % 11) % 11
    return core + ("X" if check == 10 else str(check))


def to_isbn13(isbn10: str) -> str | None:
    if len(isbn10) != 10 or not isbn10[:9].isdigit():
        return None
    core = "978" + isbn10[:9]
    total = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(core))
    return core + str((10 - total % 10) % 10)


def variants(isbn: str) -> list[str]:
    """Сам ISBN и его вторая форма (10 <-> 13)."""
    other = to_isbn10(isbn) if len(isbn) == 13 else to_isbn13(isbn)
    return [isbn] + ([other] if other else [])


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "CheckBook/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as ex:
        if ex.code == 404:  # «не найдено»
            return {}
        raise


def _from_google(item: dict) -> dict:
    info = item.get("volumeInfo", {})
    links = info.get("imageLinks") or {}
    cover = links.get("thumbnail") or links.get("smallThumbnail") or ""
    return {
        "title": info.get("title", ""),
        "author": ", ".join(info.get("authors", [])),
        "cover_url": cover.replace("http://", "https://").replace("&edge=curl", ""),
    }


def _cover_from_openlibrary(isbn: str) -> str:
    url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CheckBook/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read(1)
        return url
    except Exception:  #обложки нет
        return ""


def _google(isbn: str) -> dict | None:
    for query in (f"isbn:{isbn}", isbn):
        params = {"q": query, "maxResults": 3, "printType": "books"}
        if GOOGLE_BOOKS_KEY:
            params["key"] = GOOGLE_BOOKS_KEY
        data = _get_json("https://www.googleapis.com/books/v1/volumes?"
                         + urllib.parse.urlencode(params))
        for item in data.get("items") or []:
            ids = {i.get("identifier", "").replace("-", "")
                   for i in item.get("volumeInfo", {}).get("industryIdentifiers", [])}
            # обычный текстовый запрос принимаем, только если это та же книга
            if query.startswith("isbn:") or isbn in ids:
                return _from_google(item)
    return None


def _openlibrary(isbn: str) -> dict | None:
    key = f"ISBN:{isbn}"
    data = _get_json(
        f"https://openlibrary.org/api/books?bibkeys={key}&format=json&jscmd=data")
    info = data.get(key)
    if not info:
        return None
    cover = info.get("cover") or {}
    return {
        "title": info.get("title", ""),
        "author": ", ".join(a["name"] for a in info.get("authors", [])),
        "cover_url": cover.get("large") or cover.get("medium") or "",
    }


def _openlibrary_edition(isbn: str) -> dict | None:
    ed = _get_json(f"https://openlibrary.org/isbn/{isbn}.json")
    if not ed.get("title"):
        return None
    authors = []
    for a in (ed.get("authors") or [])[:3]:
        if a.get("key"):
            name = _get_json(f"https://openlibrary.org{a['key']}.json").get("name")
            if name:
                authors.append(name)
    covers = ed.get("covers") or []
    cover = (f"https://covers.openlibrary.org/b/id/{covers[0]}-M.jpg"
             if covers and covers[0] > 0 else "")
    return {"title": ed["title"], "author": ", ".join(authors), "cover_url": cover}


def _openlibrary_search(isbn: str) -> dict | None:
    data = _get_json(
        f"https://openlibrary.org/search.json?q={isbn}&limit=1&fields=title,author_name,cover_i")
    docs = data.get("docs") or []
    if not docs:
        return None
    d = docs[0]
    cover = (f"https://covers.openlibrary.org/b/id/{d['cover_i']}-M.jpg"
             if d.get("cover_i") else "")
    return {
        "title": d.get("title", ""),
        "author": ", ".join(d.get("author_name", [])),
        "cover_url": cover,
    }


SOURCES = (
    ("Google Books", _google),
    ("Open Library", _openlibrary),
    ("Open Library (издание)", _openlibrary_edition),
    ("Open Library (поиск)", _openlibrary_search),
)


def _find_sync(isbn: str) -> tuple[dict | None, str | None]:
    #Возвращает (данные, текст ошибки). Оба None: книги нет ни в одном источнике.
    errors = []
    for code in variants(isbn):
        for name, source in SOURCES:
            try:
                info = source(code)
                if info and info.get("title"):
                    if not info.get("cover_url"):
                        for c in variants(isbn):
                            info["cover_url"] = _cover_from_openlibrary(c)
                            if info["cover_url"]:
                                break
                    return info, None
            except Exception as ex:
                errors.append(f"{name}: {ex}")
    return None, "; ".join(dict.fromkeys(errors)) or None


async def find_book(isbn: str) -> tuple[dict | None, str | None]:
    return await asyncio.to_thread(_find_sync, isbn)