from datetime import date, time
from uuid import uuid4
from .especialista import Especialista
from .servicio import Servicio

class Reserva:
    """Clase que representa una reserva en el sistema."""

    def __init__(self, cliente: str, servicio: Servicio, especialista: Especialista,
                 fecha: date, hora: time, id: str = None, estado: str = "activa"):
        self.id = id or str(uuid4())
        self.cliente = cliente
        self.servicio = servicio
        self.especialista = especialista
        self.fecha = fecha
        self.hora = hora
        self.estado = estado  # "activa", "cancelada"

    def __str__(self) -> str:
        return (f"Reserva {self.id}: {self.servicio.nombre} con {self.especialista.nombre} "
                f"{self.especialista.apellido} - {self.fecha} {self.hora} ({self.estado})")

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para persistencia."""
        return {
            'id': self.id,
            'cliente': self.cliente,
            'servicio': self.servicio.to_dict(),
            'especialista': self.especialista.to_dict(),
            'fecha': self.fecha.isoformat(),
            'hora': self.hora.isoformat(),
            'estado': self.estado
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Reserva':
        """Crea un objeto desde un diccionario."""
        servicio = Servicio.from_dict(data['servicio'])
        especialista = Especialista.from_dict(data['especialista'])
        return cls(
            id=data['id'],
            cliente=data['cliente'],
            servicio=servicio,
            especialista=especialista,
            fecha=date.fromisoformat(data['fecha']),
            hora=time.fromisoformat(data['hora']),
            estado=data['estado']
        )