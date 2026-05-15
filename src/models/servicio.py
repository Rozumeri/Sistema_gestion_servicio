"""Modelo de Servicio.

Define la entidad que representa un servicio ofrecido en el sistema.
"""

class Servicio:
    """Representa un servicio disponible para reserva."""

    def __init__(self, nombre: str, duracion: int, costo: float, especialistas: list = None):
        self.nombre = nombre
        self.duracion = duracion
        self.costo = costo
        self.especialistas = especialistas or []

    def __str__(self) -> str:
        especialistas_texto = ', '.join(self.especialistas) if self.especialistas else 'Sin especialistas asignados'
        return f"{self.nombre} - {self.duracion}min - ${self.costo:.2f} - Especialistas: {especialistas_texto}"

    def to_dict(self) -> dict:
        """Convierte el servicio en un diccionario."""
        return {
            'nombre': self.nombre,
            'duracion': self.duracion,
            'costo': self.costo,
            'especialistas': self.especialistas
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Servicio':
        """Crea una instancia de servicio desde un diccionario."""
        return cls(
            nombre=data['nombre'],
            duracion=data['duracion'],
            costo=data['costo'],
            especialistas=data.get('especialistas', [])
        )
