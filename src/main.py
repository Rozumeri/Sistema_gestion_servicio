#!/usr/bin/env python3
"""
Sistema de Gestión de Servicios
Punto de entrada principal de la aplicación.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.validaciones_service import ValidacionesService
from services.reservas_service import ReservasService
from services.servicios_service import ServiciosService
from services.especialistas_service import EspecialistasService
from ui.admin_menu import EmpleadoMenu


def main():
    """Inicializa los servicios y ejecuta el menú principal.

    La función principal crea las instancias de los servicios de validación,
    reservas, servicios y especialistas. Después, arma el menú del sistema y
    arranca la interacción por consola.
    """

    validaciones_service = ValidacionesService()
    reservas_service = ReservasService(validaciones_service)
    servicios_service = ServiciosService(validaciones_service, reservas_service)
    especialistas_service = EspecialistasService(validaciones_service, reservas_service)

    empleado_menu = EmpleadoMenu(reservas_service, servicios_service, especialistas_service)
    empleado_menu.mostrar_menu()


if __name__ == "__main__":
    main()
