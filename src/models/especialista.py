from typing import List
from datetime import date, time
from uuid import uuid4

class Especialista:
    """Clase que representa a un especialista en el sistema."""

    def __init__(self, cedula: str, nombre: str, apellido: str, telefono: str, email: str):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} (Cédula: {self.cedula})"

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para persistencia."""
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Especialista':
        """Crea un objeto desde un diccionario."""
        return cls(
            cedula=data['cedula'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            email=data['email']
        )