"""
    Inicializa o Flet na sua rota inicial. Inicializa a lógica de controle, define título e tema.

"""

import flet as ft
import controle as con

def main(page: ft.Page):
    con.init(page)
    page.title = "Sistema de Cadastro"
    page.on_route_change = con.controle_de_rota
    page.theme_mode = "light"
    page.go('1')

ft.app(target=main)