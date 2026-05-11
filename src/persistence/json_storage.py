import json
import os
from typing import List, Optional
from .database import Database
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.especialista import Especialista
from models.servicio import Servicio
from models.reserva import Reserva

class JSONStorage(Database):
    """Implementación de persistencia usando archivos JSON."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_dir()
        self.especialistas_file = os.path.join(data_dir, "especialistas.json")
        self.servicios_file = os.path.join(data_dir, "servicios.json")
        self.reservas_file = os.path.join(data_dir, "reservas.json")

    def _ensure_data_dir(self):
        """Asegura que el directorio de datos existe."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _load_json(self, file_path: str) -> list:
        """Carga datos desde un archivo JSON."""
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_json(self, file_path: str, data: list) -> None:
        """Guarda datos en un archivo JSON."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Métodos para Especialistas
    def guardar_especialista(self, especialista: Especialista) -> None:
        especialistas = self._load_json(self.especialistas_file)
        # Remover si ya existe
        especialistas = [e for e in especialistas if e['cedula'] != especialista.cedula]
        especialistas.append(especialista.to_dict())
        self._save_json(self.especialistas_file, especialistas)

    def obtener_especialistas(self) -> List[Especialista]:
        data = self._load_json(self.especialistas_file)
        return [Especialista.from_dict(item) for item in data]

    def obtener_especialista_por_cedula(self, cedula: str) -> Optional[Especialista]:
        especialistas = self.obtener_especialistas()
        return next((e for e in especialistas if e.cedula == cedula), None)

    def eliminar_especialista(self, cedula: str) -> bool:
        especialistas = self._load_json(self.especialistas_file)
        original_count = len(especialistas)
        especialistas = [e for e in especialistas if e['cedula'] != cedula]
        if len(especialistas) < original_count:
            self._save_json(self.especialistas_file, especialistas)
            return True
        return False

    # Métodos para Servicios
    def guardar_servicio(self, servicio: Servicio) -> None:
        servicios = self._load_json(self.servicios_file)
        # Remover si ya existe
        servicios = [s for s in servicios if s['nombre'] != servicio.nombre]
        servicios.append(servicio.to_dict())
        self._save_json(self.servicios_file, servicios)

    def obtener_servicios(self) -> List[Servicio]:
        data = self._load_json(self.servicios_file)
        return [Servicio.from_dict(item) for item in data]

    def obtener_servicio_por_nombre(self, nombre: str) -> Optional[Servicio]:
        servicios = self.obtener_servicios()
        return next((s for s in servicios if s.nombre == nombre), None)

    def eliminar_servicio(self, nombre: str) -> bool:
        servicios = self._load_json(self.servicios_file)
        original_count = len(servicios)
        servicios = [s for s in servicios if s['nombre'] != nombre]
        if len(servicios) < original_count:
            self._save_json(self.servicios_file, servicios)
            return True
        return False

    # Métodos para Reservas
    def guardar_reserva(self, reserva: Reserva) -> None:
        reservas = self._load_json(self.reservas_file)
        # Remover si ya existe
        reservas = [r for r in reservas if r['id'] != reserva.id]
        reservas.append(reserva.to_dict())
        self._save_json(self.reservas_file, reservas)

    def obtener_reservas(self) -> List[Reserva]:
        data = self._load_json(self.reservas_file)
        return [Reserva.from_dict(item) for item in data]

    def obtener_reservas_por_cliente(self, cliente: str) -> List[Reserva]:
        reservas = self.obtener_reservas()
        return [r for r in reservas if r.cliente == cliente]

    def obtener_reserva_por_id(self, id: str) -> Optional[Reserva]:
        reservas = self.obtener_reservas()
        return next((r for r in reservas if r.id == id), None)

    def actualizar_reserva(self, reserva: Reserva) -> None:
        self.guardar_reserva(reserva)

    def eliminar_reserva(self, id: str) -> bool:
        reservas = self._load_json(self.reservas_file)
        original_count = len(reservas)
        reservas = [r for r in reservas if r['id'] != id]
        if len(reservas) < original_count:
            self._save_json(self.reservas_file, reservas)
            return True
        return False