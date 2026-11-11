import io

import flet as ft
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
from theme.theme import get_theme


def _jpeg(img: Image.Image, quality: int = 85) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def crop_view(page: ft.Page, data: bytes, on_done, on_back,
              x=(35, 65), y=(0, 100)) -> ft.Control:
    """Экран обрезки. x и y: начальные границы в процентах (слева-справа, сверху-снизу)."""
    t = get_theme(page)

    image = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    image.thumbnail((1600, 1600))
    state = {"img": image, "x": x, "y": y}

    def rect(img: Image.Image) -> tuple[int, int, int, int]:
        w, h = img.size
        (left, right), (top, bottom) = state["x"], state["y"]
        return (int(w * left / 100), int(h * top / 100),
                int(w * right / 100), int(h * bottom / 100))

    def preview_bytes() -> bytes:
        """Фото, где вне рамки затемнено: видно, что останется."""
        view = state["img"].copy()
        view.thumbnail((800, 800))
        r = rect(view)
        dim = ImageEnhance.Brightness(view).enhance(0.35)
        dim.paste(view.crop(r), r[:2])
        ImageDraw.Draw(dim).rectangle(r, outline=(255, 255, 255), width=4)
        return _jpeg(dim, 70)

    result = ft.Image(src=preview_bytes(), fit=ft.BoxFit.CONTAIN, height=380)

    def redraw():
        result.src = preview_bytes()
        result.update()

    def on_x(e):
        state["x"] = (e.control.start_value, e.control.end_value)
        redraw()

    def on_y(e):
        state["y"] = (e.control.start_value, e.control.end_value)
        redraw()

    def rotate(e):
        state["img"] = state["img"].rotate(-90, expand=True)
        redraw()

    def done(e):
        img = state["img"]
        on_done(_jpeg(img.crop(rect(img)), 90))

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            controls=[
                ft.Row([
                    ft.Button(content="Назад", on_click=lambda e: on_back(),
                              style=t.primary_button_style),
                    ft.Button(content="Повернуть", on_click=rotate,
                              style=t.primary_button_style),
                ]),
                result,
                ft.Text("Слева и справа", style=t.book_card_subtitle),
                ft.RangeSlider(min=0, max=100, start_value=x[0], end_value=x[1], on_change=on_x),
                ft.Text("Сверху и снизу", style=t.book_card_subtitle),
                ft.RangeSlider(min=0, max=100, start_value=y[0], end_value=y[1], on_change=on_y),
                ft.Row([ft.Button(content="Готово", expand=True, on_click=done,
                                  style=t.primary_button_style)]),
            ],
        ),
    )