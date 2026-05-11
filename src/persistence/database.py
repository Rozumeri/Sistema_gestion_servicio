from abc import ABC, abstractmethod
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.especialista import Especialista
from models.servicio import Servicio
from models.reserva import Reserva

class Database(ABC):
    """Interfaz abstracta para la capa de persistencia."""

    @abstractmethod
    def guardar_especialista(self, especialista: Especialista) -> None:
        """Guarda un especialista."""
        pass

    @abstractmethod
    def obtener_especialistas(self) -> List[Especialista]:
        """Obtiene todos los especialistas."""
        pass

    @abstractmethod
    def obtener_especialista_por_cedula(self, cedula: str) -> Optional[Especialista]:
        """Obtiene un especialista por cédula."""
        pass

    @abstractmethod
    def eliminar_especialista(self, cedula: str) -> bool:
        """Elimina un especialista por cédula."""
        pass

    @abstractmethod
    def guardar_servicio(self, servicio: Servicio) -> None:
        """Guarda un servicio."""
        pass

    @abstractmethod
    def obtener_servicios(self) -> List[Servicio]:
        """Obtiene todos los servicios."""
        pass

    @abstractmethod
    def obtener_servicio_por_nombre(self, nombre: str) -> Optional[Servicio]:
        """Obtiene un servicio por nombre."""
        pass

    @abstractmethod
    def eliminar_servicio(self, nombre: str) -> bool:
        """Elimina un servicio por nombre."""
        pass

    @abstractmethod
    def guardar_reserva(self, reserva: Reserva) -> None:
        """Guarda una reserva."""
        pass

    @abstractmethod
    def obtener_reservas(self) -> List[Reserva]:
        """Obtiene todas las reservas."""
        pass

    @abstractmethod
    def obtener_reservas_por_cliente(self, cliente: str) -> List[Reserva]:
        """Obtiene reservas de un cliente."""
        pass

    @abstractmethod
    def obtener_reserva_por_id(self, id: str) -> Optional[Reserva]:
        """Obtiene una reserva por ID."""
        pass

    @abstractmethod
    def actualizar_reserva(self, reserva: Reserva) -> None:
        """Actualiza una reserva."""
        pass

    @abstractmethod
    def eliminar_reserva(self, id: str) -> bool:
        """Elimina una reserva por ID."""
        pass