from dataclasses import dataclass

READ = "Прочитано"
PLANNED = "Запланировано"
PROCESSING = "В процессе"


@dataclass
class Book:
    title: str
    author: str
    status: str = PLANNED
    notes: str = ""
    rating: int = 0
    id: int | None = None      # None = книга ещё не сохранена в базе
    isbn: str = ""
    cover_url: str = ""
    spine_path: str = ""
    cover_path: str = ""      