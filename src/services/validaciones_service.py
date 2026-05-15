from datetime import datetime, timedelta


class ValidacionesService:
    """Servicio para validaciones de negocio."""

    def validar_disponibilidad(self, especialista, fecha: str, hora: str, duracion_minutos: int,
                               reservas: list, reserva_id: str = None) -> bool:
        """Valida si un horario está disponible para un especialista."""
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
        """Valida si se puede eliminar un especialista."""
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.especialista.cedula == cedula and
                    reserva.estado == "activa" and
                    datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False

        return True

    def validar_restricciones_eliminacion_servicio(self, nombre: str, reservas: list) -> bool:
        """Valida si se puede eliminar un servicio."""
        ahora = datetime.now()

        for reserva in reservas:
            if (reserva.servicio.nombre == nombre and
                    reserva.estado == "activa" and
                    datetime.combine(reserva.fecha, reserva.hora) > ahora):
                return False

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
