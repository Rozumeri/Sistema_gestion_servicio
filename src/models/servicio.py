class Servicio:
    """Clase que representa un servicio en el sistema."""

    def __init__(self, nombre: str, duracion: int, costo: float, especialistas: list = None):
        self.nombre = nombre
        self.duracion = duracion  # en minutos
        self.costo = costo
        self.especialistas = especialistas or []

    def __str__(self) -> str:
        return f"{self.nombre} - {self.duracion}min - ${self.costo:.2f} - Especialistas: {', '.join(self.especialistas)}"

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para persistencia."""
        return {
            'nombre': self.nombre,
            'duracion': self.duracion,
            'costo': self.costo,
            'especialistas': self.especialistas
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Servicio':
        """Crea un objeto desde un diccionario."""
        return cls(
            nombre=data['nombre'],
            duracion=data['duracion'],
            costo=data['costo'],
            especialistas=data['especialistas']
        )