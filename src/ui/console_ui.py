import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.cliente_menu import ClienteMenu
from ui.admin_menu import AdminMenu

class ConsoleUI:
    """Interfaz principal de usuario por consola."""

    def __init__(self, cliente_menu: ClienteMenu, admin_menu: AdminMenu):
        self.cliente_menu = cliente_menu
        self.admin_menu = admin_menu

    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal del sistema."""
        while True:
            print("\n" + "="*50)
            print("Bienvenido al Sistema de Gestión de Servicios")
            print("="*50)
            print("1. Ingresar como Cliente")
            print("2. Ingresar como Administrador")
            print("3. Salir")
            print("-"*50)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.cliente_menu.mostrar_menu()
            elif opcion == "2":
                self.admin_menu.mostrar_menu()
            elif opcion == "3":
                print("¡Gracias por usar el sistema!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def limpiar_pantalla(self) -> None:
        """Limpia la pantalla de la consola."""
        print("\n" * 50)  # Simulación simple de limpiar pantalla