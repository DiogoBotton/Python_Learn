import flet as ft
from control import ControleDePais

def Main(page: ft.Page):
    page.title = "Configuração de Controle de Pais"
    page.window.width = 400
    page.window.height = 600
    page.theme_mode = ft.ThemeMode.SYSTEM
        
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.CONTROL_POINT, label="Controle de Uso"),
            ft.NavigationBarDestination(icon=ft.icons.BADGE_OUTLINED, label="Recompensas")
        ]
    )
    
    routes = {
        "/": ft.View(
            "/",
            [
                navigation_bar,
                ControleDePais()
            ]
        ),
        "/reward": ft.View(
            "/reward",
            [
                navigation_bar,
                ft.Text("Reward")
            ]
        )
    }
    
    def on_route_change(e):
        view_selected = "/" if e.control.selected_index == 0 else "/reward"
        page.go(view_selected)
    
    navigation_bar.on_change = on_route_change
    
    def route_change(route):
        page.views.clear()
        page.views.append(routes[page.route])
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=Main)