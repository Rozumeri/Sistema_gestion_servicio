from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.especialista import Especialista
from persistence.database import Database
from services.validaciones_service import ValidacionesService

class EspecialistasService:
    """Servicio para gestión de especialistas."""

    def __init__(self, database: Database, validaciones_service: ValidacionesService):
        self.database = database
        self.validaciones = validaciones_service

    def crear_especialista(self, cedula: str, nombre: str, apellido: str, telefono: str, email: str) -> Especialista:
        """Crea un nuevo especialista."""
        especialista = Especialista(cedula, nombre, apellido, telefono, email)
        self.database.guardar_especialista(especialista)
        return especialista

    def obtener_especialistas(self) -> List[Especialista]:
        """Obtiene todos los especialistas."""
        return self.database.obtener_especialistas()

    def obtener_especialista_por_cedula(self, cedula: str) -> Optional[Especialista]:
        """Obtiene un especialista por cédula."""
        return self.database.obtener_especialista_por_cedula(cedula)

    def actualizar_especialista(self, cedula: str, nombre: str = None, apellido: str = None,
                               telefono: str = None, email: str = None) -> bool:
        """Actualiza la información de un especialista."""
        especialista = self.database.obtener_especialista_por_cedula(cedula)
        if not especialista:
            return False

        if nombre:
            especialista.nombre = nombre
        if apellido:
            especialista.apellido = apellido
        if telefono:
            especialista.telefono = telefono
        if email:
            especialista.email = email

        self.database.guardar_especialista(especialista)
        return True

    def eliminar_especialista(self, cedula: str) -> bool:
        """Elimina un especialista si no tiene reservas futuras."""
        if not self.validaciones.validar_restricciones_eliminacion_especialista(cedula):
            return False  # No se puede eliminar

        return self.database.eliminar_especialista(cedula)

    def obtener_especialistas_por_servicio(self, servicio_nombre: str) -> List[Especialista]:
        """
        Obtiene especialistas que ofrecen un servicio específico.
        Nota: Esta implementación simplificada retorna todos los especialistas.
        En una versión más avanzada, habría una relación muchos-a-muchos.
        """
        return self.obtener_especialistas()