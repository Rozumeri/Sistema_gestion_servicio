from datetime import datetime, timedelta
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.reserva import Reserva
from models.especialista import Especialista
from models.servicio import Servicio
from persistence.database import Database

class ValidacionesService:
    """Servicio para validaciones de negocio."""

    def __init__(self, database: Database):
        self.database = database

    def validar_disponibilidad(self, especialista: Especialista, fecha: str, hora: str, duracion_minutos: int, reserva_id: str = None) -> bool:
        """
        Valida si un horario está disponible para un especialista.
        Retorna True si está disponible, False si hay conflicto.
        """
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_dt = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            return False

        # Calcular hora de fin
        inicio = datetime.combine(fecha_dt, hora_dt)
        fin = inicio + timedelta(minutes=duracion_minutos)

        # Obtener todas las reservas activas del especialista en esa fecha
        reservas = self.database.obtener_reservas()
        reservas_especialista = [r for r in reservas
                                if r.especialista.cedula == especialista.cedula
                                and r.fecha == fecha_dt
                                and r.estado == "activa"
                                and r.id != reserva_id]  # Excluir la reserva actual si es edición

        for reserva in reservas_especialista:
            reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
            reserva_fin = reserva_inicio + timedelta(minutes=reserva.servicio.duracion)

            # Verificar solapamiento
            if (inicio < reserva_fin and fin > reserva_inicio):
                return False

        return True

    def validar_restricciones_eliminacion_especialista(self, cedula: str) -> bool:
        """
        Valida si se puede eliminar un especialista.
        Retorna True si se puede eliminar, False si tiene reservas futuras.
        """
        reservas = self.database.obtener_reservas()
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.especialista.cedula == cedula and
                reserva.estado == "activa" and
                datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False  # Tiene reservas futuras

        return True

    def validar_restricciones_eliminacion_servicio(self, nombre: str) -> bool:
        """
        Valida si se puede eliminar un servicio.
        Retorna True si se puede eliminar, False si tiene reservas futuras.
        """
        reservas = self.database.obtener_reservas()
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.servicio.nombre == nombre and
                reserva.estado == "activa" and
                datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False  # Tiene reservas futuras

        return True

    def validar_entrada_fecha(self, fecha_str: str) -> bool:
        """Valida que una fecha tenga el formato correcto YYYY-MM-DD."""
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validar_entrada_hora(self, hora_str: str) -> bool:
        """Valida que una hora tenga el formato correcto HH:MM."""
        try:
            datetime.strptime(hora_str, '%H:%M')
            return True
        except ValueError:
            return False