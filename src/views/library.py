import flet as ft
from theme.theme import get_theme
from models import Book, READ, PLANNED



def library_view(page: ft.Page, books: list[Book], on_open, on_add) -> ft.Control:
    t = get_theme(page)
    book_list = ft.ListView(expand=True, spacing=10)

    def refresh(query: str = ""):
        query = query.lower().strip()
        book_list.controls.clear()
        for book in books:
            haystack = f"{book.title} {book.author} {book.status}".lower()
            if query in haystack:
                book_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(book.title, style=t.book_card_title),
                            subtitle=ft.Text(f"{book.author} · {book.status}", style=t.book_card_subtitle),
                        ),
                        on_click=lambda e, b=book: on_open(b),
                        **t.book_card_style,
                    )
                )

    def on_search(e):
        refresh(e.control.value)
        book_list.update()

    search_box = ft.Container(
        content=ft.TextField(
            hint_text="Поиск...",
            on_change=on_search,
            **t.search_field_style
        ) 
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        foreground_color = t.ON_PRIMARY,
        bgcolor = t.PRIMARY_DARK,
        on_click=lambda e: on_add(),
    )     

    refresh()
    return ft.Column(controls=[search_box, book_list], expand=True)