"""Modelo de Especialista.

Define la entidad especialista que ofrece los servicios en el sistema.
"""

class Especialista:
    """Representa a un especialista que atiende reservas."""

    def __init__(self, cedula: str, nombre: str, apellido: str, telefono: str, email: str):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} (Cédula: {self.cedula})"

    def to_dict(self) -> dict:
        """Convierte el especialista en un diccionario.

        Aunque el sistema actual no persiste en disco, este método sirve para
        posibles futuras extensiones y mantiene consistencia con el diseño de modelos.
        """
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Especialista':
        """Crea una instancia de especialista desde un diccionario."""
        return cls(
            cedula=data['cedula'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            email=data['email']
        )
