
import flet as ft
from widgets.rating_stars import rating_stars
from theme.theme import get_theme
from models import Book
from widgets.cover import cover_box, spine_box

def book_detail_view(page: ft.Page, book: Book, on_back, on_edit, on_delete,on_update) -> ft.Container:
    t = get_theme(page)

    def set_rating(n: int):
        book.rating = n
        on_update(book)

    def set_status(e):
        book.status = e.control.value
        on_update(book)

    def set_notes(e):
        book.notes = e.control.value or ""
        on_update(book)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row( 
                    controls=[
                        ft.Button(content="Назад",
                                width=105,
                                on_click=lambda e:on_back(),
                                style = t.primary_button_style
                        ), 
                        ft.Button(content="Изменить книгу",
                                expand=True,
                                on_click=lambda e: on_edit(),
                                style = t.primary_button_style
                        )
                    ], spacing=10,
                ),

                ft.Row( #Верх карточки с обложкой, названием, автором и статусом
                    controls=[
                        cover_box(book, t),

                        spine_box(book, t),

                        ft.Column(
                            controls=[
                                ft.Container(
                                    height=70, 
                                    width=200,
                                    content=ft.Text(
                                        book.title, 
                                        max_lines=2,
                                        style=t.book_card_title,
                                        no_wrap=False),
                                    **t.book_name_style,
                                    expand=True
                                ),
                                
                                ft.Container(
                                    height=70, 
                                    width=200,
                                    content=ft.Text(
                                        book.author, 
                                        max_lines=2,
                                        style=t.book_card_subtitle,
                                        no_wrap=False),
                                    **t.book_name_style,
                                    expand=True
                                ),
                            
                            ], #spacing=5, 
                        )
                    ],
                    spacing=8, alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),

                ft.Dropdown(
                    height=40, 
                    border_radius=5, 
                    options=[
                        ft.dropdown.Option(key="Прочитано", content=ft.Text("Прочитано", color = t.ON_PRIMARY)),
                        ft.dropdown.Option(key="Запланировано",content=ft.Text("Запланировано", color = t.ON_PRIMARY)),
                        ft.dropdown.Option(key="В процессе",content=ft.Text("В процессе", color = t.ON_PRIMARY))
                        ],
                    value=book.status,
                    on_select=set_status,
                    expand=True,
                    **t.dropdown_field_style
                ),

                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                    border_radius=10,
                    content=ft.Row(
                        controls=[
                            ft.Text("Рейтинг:", color= t.ON_PRIMARY),
                            rating_stars(
                                book.rating,
                                on_change=set_rating,
                            ),
                        ],
                    ),
                ),

                ft.Row( #Заметки
                    controls=[
                        ft.TextField(
                            label="Заметки",
                            hint_text="Любимые цитаты, впечатления, заметки...",
                            multiline=True,
                            min_lines=3,
                            max_lines=8,
                            value=book.notes,
                            on_change=set_notes,
                            **t.search_field_style
                        )
                        ]
                    ),

                ft.Row( #удаление
                    controls=[
                        ft.Button(content="Удалить",
                            style=t.danger_button_style,
                            on_click=lambda e: on_delete(),
                            expand=True
                        ),
                    ]
                )
            ]
        ) 
    ) 