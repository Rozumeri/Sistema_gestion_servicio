"""Servicio para gestión de reservas en la sesión actual.

Este módulo mantiene las reservas en memoria y ofrece operaciones CRUD.
"""

from typing import List, Optional
from datetime import date, time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.reserva import Reserva
from services.validaciones_service import ValidacionesService


class ReservasService:
    """Gestiona las reservas del sistema en memoria."""

    def __init__(self, validaciones_service: ValidacionesService):
        self.validaciones = validaciones_service
        self.reservas: List[Reserva] = []

    def crear_reserva(self, cliente: str, servicio, especialista, fecha: date, hora: time) -> Optional[Reserva]:
        """Crea una reserva si el horario está disponible."""
        fecha_str = fecha.isoformat()
        hora_str = hora.strftime('%H:%M')

        if not self.validaciones.validar_disponibilidad(especialista, fecha_str, hora_str,
                                                        servicio.duracion, self.reservas):
            return None

        reserva = Reserva(cliente, servicio, especialista, fecha, hora)
        self.reservas.append(reserva)
        return reserva

    def obtener_reservas(self) -> List[Reserva]:
        """Devuelve todas las reservas registradas en la sesión."""
        return list(self.reservas)

    def obtener_reservas_por_cliente(self, cliente: str) -> List[Reserva]:
        """Filtra reservas por nombre de cliente."""
        return [r for r in self.reservas if r.cliente == cliente]

    def obtener_reserva_por_id(self, id: str) -> Optional[Reserva]:
        """Busca una reserva por su identificador único."""
        return next((r for r in self.reservas if r.id == id), None)

    def actualizar_reserva(self, id: str, nueva_fecha: date = None, nueva_hora: time = None) -> bool:
        """Actualiza fecha y/o hora de una reserva activa."""
        reserva = self.obtener_reserva_por_id(id)
        if not reserva or reserva.estado != "activa":
            return False

        fecha = nueva_fecha or reserva.fecha
        hora = nueva_hora or reserva.hora
        fecha_str = fecha.isoformat()
        hora_str = hora.strftime('%H:%M')

        if not self.validaciones.validar_disponibilidad(reserva.especialista, fecha_str, hora_str,
                                                        reserva.servicio.duracion, self.reservas, reserva.id):
            return False

        reserva.fecha = fecha
        reserva.hora = hora
        return True

    def cancelar_reserva(self, id: str) -> bool:
        """Marca una reserva como cancelada sin eliminarla."""
        reserva = self.obtener_reserva_por_id(id)
        if not reserva or reserva.estado != "activa":
            return False

        reserva.estado = "cancelada"
        return True

    def eliminar_reserva(self, id: str) -> bool:
        """Elimina una reserva de la lista de reservas."""
        reserva = self.obtener_reserva_por_id(id)
        if not reserva:
            return False

        self.reservas.remove(reserva)
        return True

    def obtener_reservas_activas_por_especialista(self, cedula: str) -> List[Reserva]:
        """Obtiene reservas activas para un especialista específico."""
        return [r for r in self.reservas if r.especialista.cedula == cedula and r.estado == "activa"]
