import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reservas_service import ReservasService
from services.servicios_service import ServiciosService
from services.especialistas_service import EspecialistasService
from services.validaciones_service import ValidacionesService
from datetime import date, time

class ClienteMenu:
    """Menú para operaciones de cliente."""

    def __init__(self, reservas_service: ReservasService, servicios_service: ServiciosService,
                 especialistas_service: EspecialistasService, validaciones_service: ValidacionesService):
        self.reservas_service = reservas_service
        self.servicios_service = servicios_service
        self.especialistas_service = especialistas_service
        self.validaciones_service = validaciones_service

    def mostrar_menu(self) -> None:
        """Muestra el menú del cliente."""
        cliente = self._solicitar_cliente()
        if not cliente:
            return

        while True:
            print(f"\nMenú Cliente - {cliente}")
            print("="*40)
            print("1. Crear Reserva")
            print("2. Ver Mis Reservas")
            print("3. Editar Reserva")
            print("4. Cancelar Reserva")
            print("5. Volver al Menú Principal")
            print("-"*40)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._crear_reserva(cliente)
            elif opcion == "2":
                self._ver_reservas(cliente)
            elif opcion == "3":
                self._editar_reserva(cliente)
            elif opcion == "4":
                self._cancelar_reserva(cliente)
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def _solicitar_cliente(self) -> str:
        """Solicita el nombre del cliente."""
        cliente = input("Ingrese su nombre: ").strip()
        if not cliente:
            print("Nombre no válido.")
            return ""
        return cliente

    def _crear_reserva(self, cliente: str) -> None:
        """Guía al cliente para crear una reserva."""
        print("\nCrear Nueva Reserva")
        print("-"*20)

        # Seleccionar servicio
        servicios = self.servicios_service.obtener_servicios()
        if not servicios:
            print("No hay servicios disponibles.")
            return

        print("Servicios disponibles:")
        for i, servicio in enumerate(servicios, 1):
            print(f"{i}. {servicio}")

        try:
            opcion_servicio = int(input("Seleccione un servicio: ")) - 1
            if opcion_servicio < 0 or opcion_servicio >= len(servicios):
                print("Opción no válida.")
                return
            servicio = servicios[opcion_servicio]
        except ValueError:
            print("Entrada no válida.")
            return

        # Seleccionar especialista
        especialistas = self.especialistas_service.obtener_especialistas_por_servicio(servicio.nombre)
        if not especialistas:
            print("No hay especialistas disponibles para este servicio.")
            return

        print(f"\nEspecialistas disponibles para {servicio.nombre}:")
        for i, especialista in enumerate(especialistas, 1):
            print(f"{i}. {especialista}")

        try:
            opcion_especialista = int(input("Seleccione un especialista: ")) - 1
            if opcion_especialista < 0 or opcion_especialista >= len(especialistas):
                print("Opción no válida.")
                return
            especialista = especialistas[opcion_especialista]
        except ValueError:
            print("Entrada no válida.")
            return

        # Solicitar fecha y hora
        fecha_str = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        if not self.validaciones_service.validar_entrada_fecha(fecha_str):
            print("Formato de fecha incorrecto. Use YYYY-MM-DD.")
            return

        hora_str = input("Ingrese hora (HH:MM): ").strip()
        if not self.validaciones_service.validar_entrada_hora(hora_str):
            print("Formato de hora incorrecto. Use HH:MM.")
            return

        try:
            fecha = date.fromisoformat(fecha_str)
            hora = time.fromisoformat(hora_str)
        except ValueError:
            print("Fecha u hora inválida.")
            return

        # Crear reserva
        reserva = self.reservas_service.crear_reserva(cliente, servicio, especialista, fecha, hora)
        if reserva:
            print(f"\n¡Reserva creada exitosamente!")
            print(f"ID de reserva: {reserva.id}")
            print(f"Servicio: {servicio.nombre}")
            print(f"Especialista: {especialista.nombre} {especialista.apellido}")
            print(f"Fecha y hora: {fecha} {hora}")
        else:
            print("\nLo siento, el horario no está disponible. Intente con otro horario.")

    def _ver_reservas(self, cliente: str) -> None:
        """Muestra las reservas del cliente."""
        reservas = self.reservas_service.obtener_reservas_por_cliente(cliente)

        if not reservas:
            print(f"\nNo tiene reservas registradas, {cliente}.")
            return

        print(f"\nSus reservas, {cliente}:")
        print("-"*60)
        for reserva in reservas:
            print(reserva)

    def _editar_reserva(self, cliente: str) -> None:
        """Permite editar una reserva existente."""
        reservas = self.reservas_service.obtener_reservas_por_cliente(cliente)
        reservas_activas = [r for r in reservas if r.estado == "activa"]

        if not reservas_activas:
            print(f"\nNo tiene reservas activas para editar, {cliente}.")
            return

        print(f"\nSus reservas activas, {cliente}:")
        for i, reserva in enumerate(reservas_activas, 1):
            print(f"{i}. {reserva}")

        try:
            opcion = int(input("Seleccione la reserva a editar: ")) - 1
            if opcion < 0 or opcion >= len(reservas_activas):
                print("Opción no válida.")
                return
            reserva = reservas_activas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        # Solicitar nueva fecha y hora
        fecha_str = input("Nueva fecha (YYYY-MM-DD) o Enter para mantener: ").strip()
        hora_str = input("Nueva hora (HH:MM) o Enter para mantener: ").strip()

        nueva_fecha = None
        nueva_hora = None

        if fecha_str:
            if not self.validaciones_service.validar_entrada_fecha(fecha_str):
                print("Formato de fecha incorrecto.")
                return
            nueva_fecha = date.fromisoformat(fecha_str)

        if hora_str:
            if not self.validaciones_service.validar_entrada_hora(hora_str):
                print("Formato de hora incorrecto.")
                return
            nueva_hora = time.fromisoformat(hora_str)

        if self.reservas_service.actualizar_reserva(reserva.id, nueva_fecha, nueva_hora):
            print("Reserva actualizada exitosamente.")
        else:
            print("No se pudo actualizar la reserva. Verifique el nuevo horario.")

    def _cancelar_reserva(self, cliente: str) -> None:
        """Permite cancelar una reserva."""
        reservas = self.reservas_service.obtener_reservas_por_cliente(cliente)
        reservas_activas = [r for r in reservas if r.estado == "activa"]

        if not reservas_activas:
            print(f"\nNo tiene reservas activas para cancelar, {cliente}.")
            return

        print(f"\nSus reservas activas, {cliente}:")
        for i, reserva in enumerate(reservas_activas, 1):
            print(f"{i}. {reserva}")

        try:
            opcion = int(input("Seleccione la reserva a cancelar: ")) - 1
            if opcion < 0 or opcion >= len(reservas_activas):
                print("Opción no válida.")
                return
            reserva = reservas_activas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        if self.reservas_service.cancelar_reserva(reserva.id):
            print("Reserva cancelada exitosamente.")
        else:
            print("No se pudo cancelar la reserva.")