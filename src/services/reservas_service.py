from typing import List, Optional
from datetime import date, time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.reserva import Reserva
from models.servicio import Servicio
from models.especialista import Especialista
from persistence.database import Database
from services.validaciones_service import ValidacionesService

class ReservasService:
    """Servicio para gestión de reservas."""

    def __init__(self, database: Database, validaciones_service: ValidacionesService):
        self.database = database
        self.validaciones = validaciones_service

    def crear_reserva(self, cliente: str, servicio: Servicio, especialista: Especialista,
                     fecha: date, hora: time) -> Optional[Reserva]:
        """Crea una nueva reserva si el horario está disponible."""
        fecha_str = fecha.isoformat()
        hora_str = hora.strftime('%H:%M')

        if not self.validaciones.validar_disponibilidad(especialista, fecha_str, hora_str, servicio.duracion):
            return None  # Horario no disponible

        reserva = Reserva(cliente, servicio, especialista, fecha, hora)
        self.database.guardar_reserva(reserva)
        return reserva

    def obtener_reservas(self) -> List[Reserva]:
        """Obtiene todas las reservas."""
        return self.database.obtener_reservas()

    def obtener_reservas_por_cliente(self, cliente: str) -> List[Reserva]:
        """Obtiene reservas de un cliente específico."""
        return self.database.obtener_reservas_por_cliente(cliente)

    def obtener_reserva_por_id(self, id: str) -> Optional[Reserva]:
        """Obtiene una reserva por ID."""
        return self.database.obtener_reserva_por_id(id)

    def actualizar_reserva(self, id: str, nueva_fecha: date = None, nueva_hora: time = None) -> bool:
        """Actualiza fecha y hora de una reserva."""
        reserva = self.database.obtener_reserva_por_id(id)
        if not reserva or reserva.estado != "activa":
            return False

        # Si se cambia fecha/hora, validar disponibilidad
        if nueva_fecha or nueva_hora:
            fecha = nueva_fecha or reserva.fecha
            hora = nueva_hora or reserva.hora
            fecha_str = fecha.isoformat()
            hora_str = hora.strftime('%H:%M')

            if not self.validaciones.validar_disponibilidad(reserva.especialista, fecha_str, hora_str,
                                                          reserva.servicio.duracion, reserva.id):
                return False  # Nuevo horario no disponible

            reserva.fecha = fecha
            reserva.hora = hora

        self.database.actualizar_reserva(reserva)
        return True

    def cancelar_reserva(self, id: str) -> bool:
        """Cancela una reserva."""
        reserva = self.database.obtener_reserva_por_id(id)
        if not reserva or reserva.estado != "activa":
            return False

        reserva.estado = "cancelada"
        self.database.actualizar_reserva(reserva)
        return True

    def obtener_reservas_activas_por_especialista(self, cedula: str) -> List[Reserva]:
        """Obtiene reservas activas de un especialista."""
        reservas = self.database.obtener_reservas()
        return [r for r in reservas if r.especialista.cedula == cedula and r.estado == "activa"]