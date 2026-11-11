from pathlib import Path

import flet as ft


def _style(t) -> dict:
    return {**t.book_card_style, "padding": 0}


def cover_box(book, t, width: int = 100, height: int = 150, on_click=None) -> ft.Container:
    path = Path(book.cover_path) if book.cover_path else None
    if path and path.exists():
        content = ft.Image(src=path.read_bytes(), width=width, height=height, fit=ft.BoxFit.COVER)
    elif book.cover_url:
        content = ft.Image(src=book.cover_url, width=width, height=height, fit=ft.BoxFit.COVER)
    elif on_click:
        content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT, color=t.ON_PRIMARY),
                ft.Text("Фото обложки", size=11, color=t.ON_PRIMARY,
                        text_align=ft.TextAlign.CENTER),
            ],
        )
    else:
        content = ft.Icon(ft.Icons.MENU_BOOK, color=t.ON_PRIMARY)
    return ft.Container(
        width=width, height=height,
        alignment=ft.Alignment.CENTER,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=content, on_click=on_click,
        tooltip="Нажмите, чтобы сфотографировать обложку" if on_click else None,
        **_style(t),
    )


def spine_box(book, t, width: int = 20, height: int = 150, on_click=None) -> ft.Container:
    path = Path(book.spine_path) if book.spine_path else None
    content = None
    if path and path.exists():
        content = ft.Image(src=path.read_bytes(), width=width, height=height, fit=ft.BoxFit.COVER)
    return ft.Container(
        width=width, height=height,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=content, on_click=on_click,
        tooltip="Фото корешка",
        **_style(t),
    )