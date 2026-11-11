import asyncio

import flet as ft
import flet_camera as fc
from theme.theme import get_theme


def camera_view(page: ft.Page, hint: str, on_photo, on_back, auto: bool = False, guide=None):
    """
    on_photo(data) возвращает None при успехе или текст, если нужно повторить.
    auto=True: камера сама снимает кадры, пока on_photo не вернёт успех.
    guide=(ширина, высота): рамка-подсказка поверх превью.
    Возвращает (экран, start). start() вызывают после добавления экрана на страницу.
    """
    t = get_theme(page)

    overlay = None
    if guide:
        overlay = ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Container(
                width=guide[0], height=guide[1],
                border=ft.Border.all(3, ft.Colors.WHITE),
                border_radius=10,
            ),
        )

    preview = fc.Camera(expand=True, preview_enabled=True, content=overlay)
    status = ft.Text(hint, style=t.book_card_subtitle)
    shoot_btn = ft.Button(content="Снять", expand=True, disabled=True,
                          visible=not auto, style=t.primary_button_style)
    state = {"busy": False, "active": True}
    tasks = []  # ссылка на задачу, чтобы её не убрала сборка мусора

    async def auto_scan():
        await asyncio.sleep(1.5)  # даём камере сфокусироваться
        while state["active"]:
            try:
                data = await preview.take_picture()
                if not state["active"]:
                    return
                error = await on_photo(data)
            except Exception as ex:
                if state["active"]:
                    status.value = f"Ошибка камеры: {ex}"
                    page.update()
                return
            if not error:
                return
            status.value = error
            page.update()
            await asyncio.sleep(0.7)

    async def start():
        try:
            cameras = await preview.get_available_cameras()
            if not cameras:
                status.value = "Камера не найдена"
                page.update()
                return
            camera = next(
                (c for c in cameras if c.lens_direction == fc.CameraLensDirection.BACK),
                cameras[0],
            )
            await preview.initialize(
                description=camera,
                resolution_preset=fc.ResolutionPreset.HIGH,
                enable_audio=False,
            )
            shoot_btn.disabled = False
            if auto:
                tasks.append(asyncio.create_task(auto_scan()))
        except Exception as ex:
            status.value = f"Не удалось включить камеру: {ex}"
        page.update()

    async def shoot(e):
        if state["busy"]:
            return
        state["busy"] = True
        shoot_btn.disabled = True
        status.value = "Обработка..."
        page.update()
        try:
            data = await preview.take_picture()
            error = await on_photo(data)
        except Exception as ex:
            error = f"Ошибка: {ex}"
        if error:
            status.value = error
            shoot_btn.disabled = False
            state["busy"] = False
            page.update()

    shoot_btn.on_click = shoot

    def back(e):
        state["active"] = False  # останавливаем авто-сканирование
        on_back()

    view = ft.Column(
        expand=True,
        controls=[
            ft.Row([ft.Button(content="Назад", on_click=back, style=t.primary_button_style)]),
            ft.Container(expand=True, bgcolor=ft.Colors.BLACK, border_radius=8, content=preview),
            status,
            ft.Row([shoot_btn]),
        ],
    )
    return view, start