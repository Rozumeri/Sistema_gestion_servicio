"""Servicio para gestión de especialistas en la sesión actual.

Mantiene especialistas en memoria y controla operaciones CRUD básicas.
"""

from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.especialista import Especialista
from services.validaciones_service import ValidacionesService
from services.reservas_service import ReservasService


class EspecialistasService:
    """Gestiona a los especialistas disponibles en el sistema."""

    def __init__(self, validaciones_service: ValidacionesService, reservas_service: ReservasService):
        self.validaciones = validaciones_service
        self.reservas_service = reservas_service
        self.especialistas: List[Especialista] = []

    def crear_especialista(self, cedula: str, nombre: str, apellido: str,
                           telefono: str, email: str) -> Especialista:
        """Crea o sobrescribe un especialista con la misma cédula."""
        especialista = Especialista(cedula, nombre, apellido, telefono, email)
        self.especialistas = [e for e in self.especialistas if e.cedula != especialista.cedula]
        self.especialistas.append(especialista)
        return especialista

    def obtener_especialistas(self) -> List[Especialista]:
        """Devuelve todos los especialistas registrados en memoria."""
        return list(self.especialistas)

    def obtener_especialista_por_cedula(self, cedula: str) -> Optional[Especialista]:
        """Busca un especialista por cédula."""
        return next((e for e in self.especialistas if e.cedula == cedula), None)

    def actualizar_especialista(self, cedula: str, nombre: str = None, apellido: str = None,
                                telefono: str = None, email: str = None) -> bool:
        """Actualiza los datos de un especialista existente."""
        especialista = self.obtener_especialista_por_cedula(cedula)
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

        return True

    def eliminar_especialista(self, cedula: str) -> bool:
        """Elimina un especialista si no tiene reservas futuras."""
        if not self.validaciones.validar_restricciones_eliminacion_especialista(cedula,
                                                                                self.reservas_service.obtener_reservas()):
            return False

        especialista = self.obtener_especialista_por_cedula(cedula)
        if not especialista:
            return False

        self.especialistas.remove(especialista)
        return True

    def obtener_especialistas_por_servicio(self, servicio_nombre: str) -> List[Especialista]:
        """Devuelve todos los especialistas disponibles.

        La versión actual no modela relaciones directas entre especialistas y servicios.
        """
        return self.obtener_especialistas()
