"""Modelo de Especialista.

Define la entidad especialista que ofrece los servicios en el sistema.
Esta clase representa a un profesional que puede ser asignado a reservas.
"""

class Especialista:
    """Representa a un especialista que atiende reservas.

    Un especialista es un profesional identificado por su cédula, con datos de contacto
    que permiten localizarlo. Puede ser asignado a múltiples reservas, pero el sistema
    actual no valida conflictos de horario entre especialistas directamente.
    """

    def __init__(self, cedula: str, nombre: str, apellido: str, telefono: str, email: str):
        """Inicializa un especialista con sus datos personales.

        Args:
            cedula (str): Identificador único del especialista.
            nombre (str): Primer nombre del especialista.
            apellido (str): Apellido del especialista.
            telefono (str): Número de teléfono de contacto.
            email (str): Dirección de correo electrónico.
        """
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def __str__(self) -> str:
        """Devuelve una representación legible del especialista.

        Returns:
            str: Cadena con nombre completo y cédula.
        """
        return f"{self.nombre} {self.apellido} (Cédula: {self.cedula})"

    def to_dict(self) -> dict:
        """Convierte el especialista en un diccionario.

        Aunque el sistema actual no persiste en disco, este método sirve para
        posibles futuras extensiones y mantiene consistencia con el diseño de modelos.
        Facilita la serialización si se agrega persistencia.

        Returns:
            dict: Diccionario con todos los atributos del especialista.
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
        """Crea una instancia de especialista desde un diccionario.

        Args:
            data (dict): Diccionario con las claves 'cedula', 'nombre', 'apellido',
                        'telefono' y 'email'.

        Returns:
            Especialista: Nueva instancia creada desde los datos.
        """
        return cls(
            cedula=data['cedula'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            email=data['email']
        )
