from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.servicio import Servicio
from persistence.database import Database
from services.validaciones_service import ValidacionesService

class ServiciosService:
    """Servicio para gestión de servicios."""

    def __init__(self, database: Database, validaciones_service: ValidacionesService):
        self.database = database
        self.validaciones = validaciones_service

    def crear_servicio(self, nombre: str, duracion: int, costo: float) -> Servicio:
        """Crea un nuevo servicio."""
        servicio = Servicio(nombre, duracion, costo)
        self.database.guardar_servicio(servicio)
        return servicio

    def obtener_servicios(self) -> List[Servicio]:
        """Obtiene todos los servicios."""
        return self.database.obtener_servicios()

    def obtener_servicio_por_nombre(self, nombre: str) -> Optional[Servicio]:
        """Obtiene un servicio por nombre."""
        return self.database.obtener_servicio_por_nombre(nombre)

    def actualizar_servicio(self, nombre: str, nuevo_nombre: str = None, duracion: int = None, costo: float = None) -> bool:
        """Actualiza la información de un servicio."""
        servicio = self.database.obtener_servicio_por_nombre(nombre)
        if not servicio:
            return False

        if nuevo_nombre:
            servicio.nombre = nuevo_nombre
        if duracion is not None:
            servicio.duracion = duracion
        if costo is not None:
            servicio.costo = costo

        self.database.guardar_servicio(servicio)
        return True

    def eliminar_servicio(self, nombre: str) -> bool:
        """Elimina un servicio si no tiene reservas futuras."""
        if not self.validaciones.validar_restricciones_eliminacion_servicio(nombre):
            return False  # No se puede eliminar

        return self.database.eliminar_servicio(nombre)