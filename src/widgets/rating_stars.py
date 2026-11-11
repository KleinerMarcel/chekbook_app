import flet as ft



def rating_stars(value: int, on_change=None, size: int = 28) -> ft.Row:
    row = ft.Row(spacing=0)

    def draw(current: int):
        row.controls.clear()
        for i in range(1, 6):
            row.controls.append(
                ft.IconButton(
                    icon=ft.Icons.STAR if i <= current else ft.Icons.STAR_BORDER,
                    icon_color=ft.Colors.AMBER,
                    icon_size=size,
                    on_click=lambda e, n=i: select(n),
                )
            )

    def select(n: int):
        draw(n)
        row.update()
        if on_change:
            on_change(n)

    draw(value)
    return row
