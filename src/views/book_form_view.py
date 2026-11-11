import flet as ft
from models import Book, PLANNED
from theme.theme import get_theme
from widgets.cover import cover_box, spine_box

STATUSES = ["Прочитано", "Запланировано", "В процессе"]

def book_form_view(
    page: ft.Page,
    book: Book,
    on_save,
    on_back,
    on_scan_isbn,
    on_lookup_isbn,
    on_photo,
) -> ft.Control:
    t = get_theme(page)
    is_edit = book.id is not None

    title_field = ft.TextField(label="Название", 
                               height=70, 
                               value=book.title, 
                               **t.search_field_style)
    
    author_field = ft.TextField(label="Автор", 
                                height=70, 
                                value=book.author, 
                                **t.search_field_style)
    
    isbn_field = ft.TextField(label="ISBN",
                              value=book.isbn,  
                              **t.search_field_style)
    
    status_dropdown = ft.Dropdown(
        label="Статус",
        value=book.status or PLANNED,
        expand=True,
        options=[
            ft.dropdown.Option(key="Прочитано", content=ft.Text("Прочитано", color = t.ON_PRIMARY)),
            ft.dropdown.Option(key="Запланировано",content=ft.Text("Запланировано", color = t.ON_PRIMARY)),
            ft.dropdown.Option(key="В процессе",content=ft.Text("В процессе", color = t.ON_PRIMARY))
            ],
        border=ft.OutlineInputBorder(border_radius=8),
        **t.dropdown_field_style
    )

    def read_fields():
        """Переносит введённое в объект книги."""
        book.title = (title_field.value or "").strip()
        book.author = (author_field.value or "").strip()
        book.isbn = (isbn_field.value or "").strip()
        book.status = status_dropdown.value or PLANNED

    async def scan(e):
        read_fields()
        await on_scan_isbn(book)

    async def lookup(e):
        read_fields()
        await on_lookup_isbn(book)

    async def spine(e):
        read_fields()
        await on_photo(book, "spine")

    async def cover(e):
        read_fields()
        await on_photo(book, "cover")

    def save(e):
        read_fields()
        if not book.title:
            title_field.error_text = "Введите название"
            title_field.update()
            return
        on_save(book)

    return ft.Container(
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Изменить книгу" if is_edit else "Новая книга", style=t.new_book_title, text_align=ft.TextAlign.CENTER), 
                ft.Row(
                    spacing=10,
                    controls=[
                        cover_box(book, t, on_click=cover),
                        spine_box(book, t, on_click=spine),
                        ft.Column(expand=True, controls=[title_field, author_field]),
                    ],
                ),
                ft.Text("Нажмите на прямоугольники, чтобы сфотографировать", style=t.messege),
                status_dropdown,
                ft.Row([isbn_field, ft.IconButton(icon=ft.Icons.SEARCH, 
                                                  on_click=lookup,
                                                  icon_color = t.ON_PRIMARY,
                                                  tooltip="Найти по ISBN")]),
                ft.Row([ft.Button(content="Сканировать ISBN", expand=True,
                                  on_click=scan, style=t.primary_button_style)]),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Button(content="Отмена", expand=True,
                                  on_click=lambda e: on_back(), style=t.primary_button_style),
                        ft.Button(content="Сохранить", expand=True,
                                  on_click=save, style=t.primary_button_style),
                    ],
                ),
            ],
        ),
    )