from typing import List, Optional
from datetime import date, time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.reserva import Reserva
from services.validaciones_service import ValidacionesService


class ReservasService:
    """Servicio para gestión de reservas."""

    def __init__(self, validaciones_service: ValidacionesService):
        self.validaciones = validaciones_service
        self.reservas: List[Reserva] = []

    def crear_reserva(self, cliente: str, servicio, especialista, fecha: date, hora: time) -> Optional[Reserva]:
        """Crea una nueva reserva si el horario está disponible."""
        fecha_str = fecha.isoformat()
        hora_str = hora.strftime('%H:%M')

        if not self.validaciones.validar_disponibilidad(especialista, fecha_str, hora_str,
                                                        servicio.duracion, self.reservas):
            return None

        reserva = Reserva(cliente, servicio, especialista, fecha, hora)
        self.reservas.append(reserva)
        return reserva

    def obtener_reservas(self) -> List[Reserva]:
        """Obtiene todas las reservas."""
        return list(self.reservas)

    def obtener_reservas_por_cliente(self, cliente: str) -> List[Reserva]:
        """Obtiene reservas de un cliente específico."""
        return [r for r in self.reservas if r.cliente == cliente]

    def obtener_reserva_por_id(self, id: str) -> Optional[Reserva]:
        """Obtiene una reserva por ID."""
        return next((r for r in self.reservas if r.id == id), None)

    def actualizar_reserva(self, id: str, nueva_fecha: date = None, nueva_hora: time = None) -> bool:
        """Actualiza fecha y hora de una reserva."""
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
        """Cancela una reserva."""
        reserva = self.obtener_reserva_por_id(id)
        if not reserva or reserva.estado != "activa":
            return False

        reserva.estado = "cancelada"
        return True

    def eliminar_reserva(self, id: str) -> bool:
        """Elimina una reserva del sistema."""
        reserva = self.obtener_reserva_por_id(id)
        if not reserva:
            return False

        self.reservas.remove(reserva)
        return True

    def obtener_reservas_activas_por_especialista(self, cedula: str) -> List[Reserva]:
        """Obtiene reservas activas de un especialista."""
        return [r for r in self.reservas if r.especialista.cedula == cedula and r.estado == "activa"]
