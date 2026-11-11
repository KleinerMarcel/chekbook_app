import flet as ft
from . import light_theme
from . import dark_theme


def get_theme(page: ft.Page):
    if page.platform_brightness == ft.Brightness.DARK:
        return dark_theme
    return light_theme