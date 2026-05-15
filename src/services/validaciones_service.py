"""Servicio de validaciones de negocio.

Contiene las reglas que controlan conflictos de horarios y restricciones de eliminación.
"""

from datetime import datetime, timedelta


class ValidacionesService:
    """Encapsula validaciones comunes del dominio."""

    def validar_disponibilidad(self, especialista, fecha: str, hora: str, duracion_minutos: int,
                               reservas: list, reserva_id: str = None) -> bool:
        """Verifica si un especialista está disponible en un horario dado."""
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_dt = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            return False

        inicio = datetime.combine(fecha_dt, hora_dt)
        fin = inicio + timedelta(minutes=duracion_minutos)

        reservas_especialista = [r for r in reservas
                                 if r.especialista.cedula == especialista.cedula
                                 and r.fecha == fecha_dt
                                 and r.estado == "activa"
                                 and r.id != reserva_id]

        for reserva in reservas_especialista:
            reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
            reserva_fin = reserva_inicio + timedelta(minutes=reserva.servicio.duracion)
            if inicio < reserva_fin and fin > reserva_inicio:
                return False

        return True

    def validar_restricciones_eliminacion_especialista(self, cedula: str, reservas: list) -> bool:
        """Verifica si un especialista puede eliminarse sin reservas futuras."""
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.especialista.cedula == cedula and
                    reserva.estado == "activa" and
                    datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False

        return True

    def validar_restricciones_eliminacion_servicio(self, nombre: str, reservas: list) -> bool:
        """Verifica si un servicio puede eliminarse sin reservas futuras."""
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.servicio.nombre == nombre and
                    reserva.estado == "activa" and
                    datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False

        return True

    def validar_entrada_fecha(self, fecha_str: str) -> bool:
        """Valida que la cadena de fecha sea YYYY-MM-DD."""
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validar_entrada_hora(self, hora_str: str) -> bool:
        """Valida que la cadena de hora sea HH:MM."""
        try:
            datetime.strptime(hora_str, '%H:%M')
            return True
        except ValueError:
            return False
