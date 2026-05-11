#!/usr/bin/env python3
"""
Script para inicializar datos de ejemplo en el sistema.
Ejecutar una vez para poblar la base de datos con datos de prueba.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from persistence.json_storage import JSONStorage
from services.validaciones_service import ValidacionesService
from services.reservas_service import ReservasService
from services.servicios_service import ServiciosService
from services.especialistas_service import EspecialistasService
from datetime import date, time, timedelta

def inicializar_datos():
    """Inicializa datos de ejemplo."""
    database = JSONStorage()
    validaciones_service = ValidacionesService(database)
    reservas_service = ReservasService(database, validaciones_service)
    servicios_service = ServiciosService(database, validaciones_service)
    especialistas_service = EspecialistasService(database, validaciones_service)

    # Crear servicios de ejemplo
    print("Creando servicios de ejemplo...")
    corte_cabello = servicios_service.crear_servicio("Corte de Cabello", 30, 15.0)
    manicura = servicios_service.crear_servicio("Manicura", 45, 25.0)
    masaje = servicios_service.crear_servicio("Masaje Relajante", 60, 40.0)

    # Crear especialistas de ejemplo
    print("Creando especialistas de ejemplo...")
    maria = especialistas_service.crear_especialista("12345678", "María", "González", "555-0101", "maria@email.com")
    carlos = especialistas_service.crear_especialista("87654321", "Carlos", "Rodríguez", "555-0202", "carlos@email.com")
    ana = especialistas_service.crear_especialista("11223344", "Ana", "López", "555-0303", "ana@email.com")

    # Crear algunas reservas de ejemplo
    print("Creando reservas de ejemplo...")
    from datetime import timedelta
    hoy = date.today()
    manana = hoy + timedelta(days=1)

    # Reserva 1: Corte de cabello con María mañana a las 10:00
    reservas_service.crear_reserva("Juan Pérez", corte_cabello, maria, manana, time(10, 0))

    # Reserva 2: Manicura con Ana mañana a las 14:00
    reservas_service.crear_reserva("María García", manicura, ana, manana, time(14, 0))

    # Reserva 3: Masaje con Carlos pasado mañana a las 16:00
    pasado_manana = hoy + timedelta(days=2)
    reservas_service.crear_reserva("Pedro López", masaje, carlos, pasado_manana, time(16, 0))

    print("Datos de ejemplo inicializados exitosamente!")
    print("\nServicios disponibles:")
    for servicio in servicios_service.obtener_servicios():
        print(f"- {servicio}")

    print("\nEspecialistas disponibles:")
    for especialista in especialistas_service.obtener_especialistas():
        print(f"- {especialista}")

    print(f"\nReservas registradas: {len(reservas_service.obtener_reservas())}")

if __name__ == "__main__":
    inicializar_datos()