#!/usr/bin/env python3
"""
Sistema de Gestión de Servicios
Punto de entrada principal de la aplicación.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from persistence.json_storage import JSONStorage
from services.validaciones_service import ValidacionesService
from services.reservas_service import ReservasService
from services.servicios_service import ServiciosService
from services.especialistas_service import EspecialistasService
from ui.console_ui import ConsoleUI
from ui.cliente_menu import ClienteMenu
from ui.admin_menu import AdminMenu

def main():
    """Función principal que inicializa y ejecuta el sistema."""
    # Inicializar persistencia
    database = JSONStorage()

    # Inicializar servicios de validación
    validaciones_service = ValidacionesService(database)

    # Inicializar servicios de negocio
    reservas_service = ReservasService(database, validaciones_service)
    servicios_service = ServiciosService(database, validaciones_service)
    especialistas_service = EspecialistasService(database, validaciones_service)

    # Inicializar menús de UI
    cliente_menu = ClienteMenu(reservas_service, servicios_service, especialistas_service, validaciones_service)
    admin_menu = AdminMenu(reservas_service, servicios_service, especialistas_service)

    # Inicializar UI principal
    ui = ConsoleUI(cliente_menu, admin_menu)

    # Ejecutar el sistema
    ui.mostrar_menu_principal()

if __name__ == "__main__":
    main()