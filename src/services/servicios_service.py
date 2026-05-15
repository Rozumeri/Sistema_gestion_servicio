"""Servicio para gestión de servicios en la sesión actual.

Mantiene servicios en memoria y controla operaciones CRUD básicas.
"""

from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.servicio import Servicio
from services.validaciones_service import ValidacionesService
from services.reservas_service import ReservasService


class ServiciosService:
    """Gestiona los servicios disponibles para reserva."""

    def __init__(self, validaciones_service: ValidacionesService, reservas_service: ReservasService):
        self.validaciones = validaciones_service
        self.reservas_service = reservas_service
        self.servicios: List[Servicio] = []

    def crear_servicio(self, nombre: str, duracion: int, costo: float) -> Servicio:
        """Crea o sobrescribe un servicio con el mismo nombre."""
        servicio = Servicio(nombre, duracion, costo)
        self.servicios = [s for s in self.servicios if s.nombre != servicio.nombre]
        self.servicios.append(servicio)
        return servicio

    def obtener_servicios(self) -> List[Servicio]:
        """Devuelve todos los servicios registrados en memoria."""
        return list(self.servicios)

    def obtener_servicio_por_nombre(self, nombre: str) -> Optional[Servicio]:
        """Busca un servicio por su nombre."""
        return next((s for s in self.servicios if s.nombre == nombre), None)

    def actualizar_servicio(self, nombre: str, nuevo_nombre: str = None,
                            duracion: int = None, costo: float = None) -> bool:
        """Modifica los atributos de un servicio existente."""
        servicio = self.obtener_servicio_por_nombre(nombre)
        if not servicio:
            return False

        if nuevo_nombre:
            servicio.nombre = nuevo_nombre
        if duracion is not None:
            servicio.duracion = duracion
        if costo is not None:
            servicio.costo = costo

        return True

    def eliminar_servicio(self, nombre: str) -> bool:
        """Elimina un servicio si no existen reservas futuras asociadas."""
        if not self.validaciones.validar_restricciones_eliminacion_servicio(nombre,
                                                                            self.reservas_service.obtener_reservas()):
            return False

        servicio = self.obtener_servicio_por_nombre(nombre)
        if not servicio:
            return False

        self.servicios.remove(servicio)
        return True
