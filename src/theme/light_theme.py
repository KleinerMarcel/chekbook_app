import flet as ft

#Light theme
PRIMARY = "#E3BD8D"
PRIMARY_DARK ="#5A0116"
ON_PRIMARY= "#1E1A2D"

STAR = "#EFB356" 



book_card_style = dict(
    bgcolor= PRIMARY_DARK,
    border=ft.Border.all(2, ON_PRIMARY),
    border_radius=ft.BorderRadius.all(5),
    padding=10,
)

book_name_style = dict(
    bgcolor= PRIMARY_DARK,
    padding=10,
    alignment= ft.Alignment.CENTER,
    border_radius=5
)

book_card_title=dict(color = PRIMARY, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
book_card_subtitle=dict(color = PRIMARY, text_align=ft.TextAlign.CENTER)

new_book_title =dict(color = ON_PRIMARY, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
messege =dict(color = ON_PRIMARY, text_align=ft.TextAlign.CENTER)

primary_button_style = ft.ButtonStyle(
    bgcolor=PRIMARY_DARK,
    color=PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=10),
    padding=14,
)

danger_button_style = ft.ButtonStyle(
    bgcolor=PRIMARY_DARK,
    color=PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=10),
    padding=14,
)

search_field_style = dict(
    filled=True,
    bgcolor=PRIMARY,
    color=ON_PRIMARY,                   
    hint_style=ft.TextStyle(color=ON_PRIMARY),
    label_style=ft.TextStyle(color=ON_PRIMARY),
    border=ft.InputBorder.OUTLINE,
    border_color=ON_PRIMARY,          
    focused_border_color=ON_PRIMARY,  
    border_width=2,                   
    focused_border_width=2,           
    border_radius=5,
    expand=True                  
)

dropdown_field_style = dict(
    bgcolor= PRIMARY_DARK,
    color= ON_PRIMARY,                  
    label_style=ft.TextStyle(color=ON_PRIMARY),
    border_color=ON_PRIMARY,          
    focused_border_color=ON_PRIMARY,
)