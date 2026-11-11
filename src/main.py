import asyncio

import flet as ft
import storage
from barcode_reader import decode_isbn
from isbn import clean_isbn, find_book
from models import Book
from photos import save_photo
from theme.theme import get_theme
from views.book_detail_view import book_detail_view
from views.book_form_view import book_form_view
from views.camera_view import camera_view
from views.library import library_view


def main(page: ft.Page):
    page.title = "CheckBook"
    t = get_theme(page)
    page.bgcolor = t.PRIMARY

    storage.init_db()
    books: list[Book] = storage.get_books()

    def clear():
        page.floating_action_button = None
        page.controls.clear()

    def notify(text: str):
        page.show_dialog(ft.SnackBar(ft.Text(text)))

    # ---------- экраны ----------
    def show_library():
        clear()
        books[:] = storage.get_books()
        page.add(ft.SafeArea(
            content=library_view(page, books, on_open=open_book, on_add=show_add_book),
            expand=True,
        ))

    def open_book(book: Book):
        clear()
        page.add(ft.SafeArea(content=book_detail_view(
            page, book,
            on_back=show_library,
            on_edit=lambda: show_form(book),
            on_delete=lambda: delete_book(book),
            on_update=storage.save_book,
        )))

    def show_form(book: Book):
        clear()
        page.add(ft.SafeArea(content=book_form_view(
            page, book,
            on_save=save_from_form,
            on_back=lambda: cancel_form(book),
            on_scan_isbn=scan_isbn,
            on_lookup_isbn=lookup_isbn,
            on_photo=take_photo,
        )))

    def show_add_book():
        show_form(Book(title="", author=""))

    async def show_camera(hint: str, on_photo, on_back, **options):
        clear()
        view, start = camera_view(page, hint, on_photo, on_back, **options)
        page.add(ft.SafeArea(content=view, expand=True))
        await start()

    # ---------- действия ----------
    def save_from_form(book: Book):
        is_new = book.id is None
        storage.save_book(book)
        if is_new:
            show_library()
        else:
            open_book(book)

    def cancel_form(book: Book):
        if book.id is None:
            show_library()
        else:  # берём книгу из базы: несохранённые правки отбрасываются
            open_book(storage.get_book(book.id) or book)

    def delete_book(book: Book):
        storage.delete_book(book)
        show_library()

    async def apply_isbn(book: Book, raw: str) -> str | None:
        isbn = clean_isbn(raw)
        if not isbn:
            return "ISBN должен содержать 10 или 13 цифр"
        book.isbn = isbn
        info, error = await find_book(isbn)
        if not info:
            if error:
                return f"Не удалось получить данные ({error})"
            return "Книга с таким ISBN не найдена. Заполните данные вручную"
        book.title = info["title"] or book.title
        book.author = info["author"] or book.author
        book.cover_url = info["cover_url"] or book.cover_url
        return None

    async def lookup_isbn(book: Book):
        message = await apply_isbn(book, book.isbn)
        show_form(book)
        if message:
            notify(message)

    async def scan_isbn(book: Book):
        async def on_photo(data: bytes):
            code = await asyncio.to_thread(decode_isbn, data)
            if not code:
                return "Штрихкод не виден. Поднесите книгу ближе, чтобы он занял рамку, и держите ровно"
            message = await apply_isbn(book, code)
            show_form(book)
            if message:
                notify(message)
            return None

        await show_camera(
            "Наведите камеру на штрихкод, сканирование идёт само",
            on_photo, lambda: show_form(book),
            auto=True, guide=(300, 140),
        )

    PHOTO_KINDS = {
        # вид: (поле книги, подсказка, границы обрезки по x, по y)
        "spine": ("spine_path", "Сфотографируйте корешок книги", (35, 65), (0, 100)),
        "cover": ("cover_path", "Сфотографируйте обложку", (5, 95), (5, 95)),
    }

    async def take_photo(book: Book, kind: str):
        hint = PHOTO_KINDS[kind][1]

        async def on_photo(data: bytes):
            show_crop(book, kind, data)
            return None

        await show_camera(hint, on_photo, lambda: show_form(book))

    def show_crop(book: Book, kind: str, data: bytes):
        _, _, crop_x, crop_y = PHOTO_KINDS[kind]
        try:  
            view = crop_view(
                page, data,
                on_done=lambda jpg: finish_photo(book, kind, jpg),
                on_back=lambda: show_form(book),
                x=crop_x, y=crop_y,
            )
        except Exception as ex:
            show_form(book)
            notify(f"Не удалось открыть фото для обрезки: {ex}")
            return
        clear()
        page.add(ft.SafeArea(content=view, expand=True))

    def finish_photo(book: Book, kind: str, jpg: bytes):
        setattr(book, PHOTO_KINDS[kind][0], save_photo(jpg, kind))
        show_form(book)

    show_library()


ft.run(main)