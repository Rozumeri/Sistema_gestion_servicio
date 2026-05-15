"""Interfaz de consola para interacción con el sistema.

Provee el menú principal y los submenús para servicios, especialistas y reservas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reservas_service import ReservasService
from services.servicios_service import ServiciosService
from services.especialistas_service import EspecialistasService


class EmpleadoMenu:
    """Encapsula los menús de interacción por consola del sistema."""

    def __init__(self, reservas_service: ReservasService, servicios_service: ServiciosService,
                 especialistas_service: EspecialistasService):
        self.reservas_service = reservas_service
        self.servicios_service = servicios_service
        self.especialistas_service = especialistas_service

    def mostrar_menu(self) -> None:
        """Muestra el menú principal del sistema y gestiona la navegación."""
        while True:
            print("\nSistema de Gestión de Servicios")
            print("="*30)
            print("1. Gestionar Servicios")
            print("2. Gestionar Especialistas")
            print("3. Gestionar Reservas")
            print("4. Salir")
            print("-"*30)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._gestionar_servicios()
            elif opcion == "2":
                self._gestionar_especialistas()
            elif opcion == "3":
                self._gestionar_reservas()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def _gestionar_servicios(self) -> None:
        """Submenú para administrar servicios."""
        while True:
            print("\nGestión de Servicios")
            print("="*25)
            print("1. Agregar Servicio")
            print("2. Ver Servicios")
            print("3. Editar Servicio")
            print("4. Eliminar Servicio")
            print("5. Volver")
            print("-"*25)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._agregar_servicio()
            elif opcion == "2":
                self._ver_servicios()
            elif opcion == "3":
                self._editar_servicio()
            elif opcion == "4":
                self._eliminar_servicio()
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")

    def _agregar_servicio(self) -> None:
        """Solicita datos y crea un nuevo servicio."""
        nombre = input("Nombre del servicio: ").strip()
        if not nombre:
            print("Nombre no válido.")
            return

        try:
            duracion = int(input("Duración en minutos: "))
            costo = float(input("Costo: "))
        except ValueError:
            print("Duración o costo no válido.")
            return

        servicio = self.servicios_service.crear_servicio(nombre, duracion, costo)
        print(f"Servicio '{servicio.nombre}' agregado exitosamente.")

    def _ver_servicios(self) -> None:
        """Muestra una lista de todos los servicios registrados."""
        servicios = self.servicios_service.obtener_servicios()
        if not servicios:
            print("No hay servicios registrados.")
            return

        print("\nServicios registrados:")
        print("-"*40)
        for servicio in servicios:
            print(servicio)

    def _editar_servicio(self) -> None:
        """Permite editar un servicio existente."""
        servicios = self.servicios_service.obtener_servicios()
        if not servicios:
            print("No hay servicios para editar.")
            return

        print("Servicios disponibles:")
        for i, servicio in enumerate(servicios, 1):
            print(f"{i}. {servicio}")

        try:
            opcion = int(input("Seleccione servicio a editar: ")) - 1
            if opcion < 0 or opcion >= len(servicios):
                print("Opción no válida.")
                return
            servicio = servicios[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        nuevo_nombre = input(f"Nuevo nombre (actual: {servicio.nombre}) o Enter: ").strip() or servicio.nombre
        try:
            nueva_duracion = input(f"Nueva duración (actual: {servicio.duracion}) o Enter: ").strip()
            nueva_duracion = int(nueva_duracion) if nueva_duracion else servicio.duracion

            nuevo_costo = input(f"Nuevo costo (actual: ${servicio.costo:.2f}) o Enter: ").strip()
            nuevo_costo = float(nuevo_costo) if nuevo_costo else servicio.costo
        except ValueError:
            print("Valor numérico no válido.")
            return

        if self.servicios_service.actualizar_servicio(servicio.nombre, nuevo_nombre, nueva_duracion, nuevo_costo):
            print("Servicio actualizado exitosamente.")
        else:
            print("No se pudo actualizar el servicio.")

    def _eliminar_servicio(self) -> None:
        """Permite eliminar un servicio si no tiene reservas futuras."""
        servicios = self.servicios_service.obtener_servicios()
        if not servicios:
            print("No hay servicios para eliminar.")
            return

        print("Servicios disponibles:")
        for i, servicio in enumerate(servicios, 1):
            print(f"{i}. {servicio}")

        try:
            opcion = int(input("Seleccione servicio a eliminar: ")) - 1
            if opcion < 0 or opcion >= len(servicios):
                print("Opción no válida.")
                return
            servicio = servicios[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        if self.servicios_service.eliminar_servicio(servicio.nombre):
            print("Servicio eliminado exitosamente.")
        else:
            print("No se puede eliminar el servicio porque tiene reservas futuras o no existe.")

    def _gestionar_especialistas(self) -> None:
        """Submenú para gestionar especialistas."""
        while True:
            print("\nGestión de Especialistas")
            print("="*28)
            print("1. Agregar Especialista")
            print("2. Ver Especialistas")
            print("3. Editar Especialista")
            print("4. Eliminar Especialista")
            print("5. Volver")
            print("-"*28)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._agregar_especialista()
            elif opcion == "2":
                self._ver_especialistas()
            elif opcion == "3":
                self._editar_especialista()
            elif opcion == "4":
                self._eliminar_especialista()
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")

    def _agregar_especialista(self) -> None:
        """Solicita datos y agrega un especialista nuevo."""
        cedula = input("Cédula: ").strip()
        if not cedula:
            print("Cédula no válida.")
            return

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        telefono = input("Teléfono: ").strip()
        email = input("Email: ").strip()

        if not all([nombre, apellido, telefono, email]):
            print("Todos los campos son obligatorios.")
            return

        especialista = self.especialistas_service.crear_especialista(cedula, nombre, apellido, telefono, email)
        print(f"Especialista '{especialista.nombre} {especialista.apellido}' agregado exitosamente.")

    def _ver_especialistas(self) -> None:
        """Lista todos los especialistas disponibles."""
        especialistas = self.especialistas_service.obtener_especialistas()
        if not especialistas:
            print("No hay especialistas registrados.")
            return

        print("\nEspecialistas registrados:")
        print("-"*50)
        for especialista in especialistas:
            print(f"{especialista} - Tel: {especialista.telefono} - Email: {especialista.email}")

    def _editar_especialista(self) -> None:
        """Edita un especialista existente."""
        especialistas = self.especialistas_service.obtener_especialistas()
        if not especialistas:
            print("No hay especialistas para editar.")
            return

        print("Especialistas disponibles:")
        for i, especialista in enumerate(especialistas, 1):
            print(f"{i}. {especialista}")

        try:
            opcion = int(input("Seleccione especialista a editar: ")) - 1
            if opcion < 0 or opcion >= len(especialistas):
                print("Opción no válida.")
                return
            especialista = especialistas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        nuevo_nombre = input(f"Nuevo nombre (actual: {especialista.nombre}) o Enter: ").strip() or especialista.nombre
        nuevo_apellido = input(f"Nuevo apellido (actual: {especialista.apellido}) o Enter: ").strip() or especialista.apellido
        nuevo_telefono = input(f"Nuevo teléfono (actual: {especialista.telefono}) o Enter: ").strip() or especialista.telefono
        nuevo_email = input(f"Nuevo email (actual: {especialista.email}) o Enter: ").strip() or especialista.email

        if self.especialistas_service.actualizar_especialista(especialista.cedula, nuevo_nombre,
                                                               nuevo_apellido, nuevo_telefono, nuevo_email):
            print("Especialista actualizado exitosamente.")
        else:
            print("No se pudo actualizar el especialista.")

    def _eliminar_especialista(self) -> None:
        """Elimina un especialista si no tiene reservas futuras."""
        especialistas = self.especialistas_service.obtener_especialistas()
        if not especialistas:
            print("No hay especialistas para eliminar.")
            return

        print("Especialistas disponibles:")
        for i, especialista in enumerate(especialistas, 1):
            print(f"{i}. {especialista}")

        try:
            opcion = int(input("Seleccione especialista a eliminar: ")) - 1
            if opcion < 0 or opcion >= len(especialistas):
                print("Opción no válida.")
                return
            especialista = especialistas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        if self.especialistas_service.eliminar_especialista(especialista.cedula):
            print("Especialista eliminado exitosamente.")
        else:
            print("No se puede eliminar el especialista porque tiene reservas futuras o no existe.")

    def _gestionar_reservas(self) -> None:
        """Submenú con acciones sobre reservas."""
        while True:
            print("\nGestión de Reservas")
            print("="*25)
            print("1. Crear Reserva")
            print("2. Ver Reservas")
            print("3. Editar Reserva")
            print("4. Cancelar Reserva")
            print("5. Eliminar Reserva")
            print("6. Volver")
            print("-"*25)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._crear_reserva()
            elif opcion == "2":
                self._ver_reservas()
            elif opcion == "3":
                self._editar_reserva()
            elif opcion == "4":
                self._cancelar_reserva()
            elif opcion == "5":
                self._eliminar_reserva()
            elif opcion == "6":
                break
            else:
                print("Opción no válida.")

    def _crear_reserva(self) -> None:
        """Solicita los datos de reserva y crea una nueva reserva."""
        cliente = input("Nombre del cliente: ").strip()
        if not cliente:
            print("Nombre no válido.")
            return

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

        fecha_str = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        if not self.reservas_service.validaciones.validar_entrada_fecha(fecha_str):
            print("Formato de fecha incorrecto. Use YYYY-MM-DD.")
            return

        hora_str = input("Ingrese hora (HH:MM): ").strip()
        if not self.reservas_service.validaciones.validar_entrada_hora(hora_str):
            print("Formato de hora incorrecto. Use HH:MM.")
            return

        try:
            from datetime import date, time
            fecha = date.fromisoformat(fecha_str)
            hora = time.fromisoformat(hora_str)
        except ValueError:
            print("Fecha u hora inválida.")
            return

        reserva = self.reservas_service.crear_reserva(cliente, servicio, especialista, fecha, hora)
        if reserva:
            print(f"\nReserva creada exitosamente. ID: {reserva.id}")
        else:
            print("No se pudo crear la reserva. El horario no está disponible.")

    def _ver_reservas(self) -> None:
        """Muestra todas las reservas existentes."""
        reservas = self.reservas_service.obtener_reservas()
        if not reservas:
            print("No hay reservas registradas.")
            return

        print("\nReservas registradas:")
        print("-"*80)
        for reserva in reservas:
            print(reserva)

    def _editar_reserva(self) -> None:
        """Permite modificar fecha y/o hora de una reserva activa."""
        reservas = self.reservas_service.obtener_reservas()
        if not reservas:
            print("No hay reservas para editar.")
            return

        print("Reservas disponibles:")
        for i, reserva in enumerate(reservas, 1):
            print(f"{i}. {reserva}")

        try:
            opcion = int(input("Seleccione reserva a editar: ")) - 1
            if opcion < 0 or opcion >= len(reservas):
                print("Opción no válida.")
                return
            reserva = reservas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        fecha_str = input(f"Nueva fecha (actual: {reserva.fecha}) o Enter: ").strip()
        hora_str = input(f"Nueva hora (actual: {reserva.hora}) o Enter: ").strip()

        nueva_fecha = None
        nueva_hora = None

        if fecha_str:
            if not self.reservas_service.validaciones.validar_entrada_fecha(fecha_str):
                print("Formato de fecha incorrecto.")
                return
            from datetime import date
            nueva_fecha = date.fromisoformat(fecha_str)

        if hora_str:
            if not self.reservas_service.validaciones.validar_entrada_hora(hora_str):
                print("Formato de hora incorrecto.")
                return
            from datetime import time
            nueva_hora = time.fromisoformat(hora_str)

        if self.reservas_service.actualizar_reserva(reserva.id, nueva_fecha, nueva_hora):
            print("Reserva actualizada exitosamente.")
        else:
            print("No se pudo actualizar la reserva. Verifique el horario.")

    def _cancelar_reserva(self) -> None:
        """Marca una reserva activa como cancelada."""
        reservas = [r for r in self.reservas_service.obtener_reservas() if r.estado == "activa"]
        if not reservas:
            print("No hay reservas activas para cancelar.")
            return

        print("Reservas activas:")
        for i, reserva in enumerate(reservas, 1):
            print(f"{i}. {reserva}")

        try:
            opcion = int(input("Seleccione reserva a cancelar: ")) - 1
            if opcion < 0 or opcion >= len(reservas):
                print("Opción no válida.")
                return
            reserva = reservas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        if self.reservas_service.cancelar_reserva(reserva.id):
            print("Reserva cancelada exitosamente.")
        else:
            print("No se pudo cancelar la reserva.")

    def _eliminar_reserva(self) -> None:
        """Elimina una reserva de la sesión actual."""
        reservas = self.reservas_service.obtener_reservas()
        if not reservas:
            print("No hay reservas para eliminar.")
            return

        print("Reservas disponibles:")
        for i, reserva in enumerate(reservas, 1):
            print(f"{i}. {reserva}")

        try:
            opcion = int(input("Seleccione reserva a eliminar: ")) - 1
            if opcion < 0 or opcion >= len(reservas):
                print("Opción no válida.")
                return
            reserva = reservas[opcion]
        except ValueError:
            print("Entrada no válida.")
            return

        if self.reservas_service.eliminar_reserva(reserva.id):
            print("Reserva eliminada exitosamente.")
        else:
            print("No se pudo eliminar la reserva.")
