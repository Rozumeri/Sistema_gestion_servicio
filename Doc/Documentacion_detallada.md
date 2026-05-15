# Documentación detallada del Sistema de Gestión de Servicios

## Descripción general

Este sistema es una aplicación de consola escrita en Python que permite gestionar servicios, especialistas y reservas dentro de una única sesión de ejecución.

El diseño actual es de tipo "runtime-only": no hay ninguna persistencia en disco ni base de datos. Todas las entidades se almacenan en listas en memoria y se pierden cuando el proceso finaliza.

El usuario esperado es un empleado administrativo. No existe login ni múltiples roles. La aplicación inicia directamente en el menú principal del empleado, sin una pantalla de bienvenida o selección de usuario previa.

## Objetivo del proyecto

- Administrar servicios ofrecidos.
- Administrar especialistas que realizan los servicios.
- Registrar reservas asociadas a servicios y especialistas.
- Validar conflictos de horario y restricciones de eliminación.
- Mantener la aplicación simple y autocontenida en memoria.

## Estructura del proyecto

### Carpetas principales

- `src/`: código fuente principal del proyecto.
- `Doc/`: documentación del proyecto.

### Contenido de `src/`

- `src/main.py`: punto de entrada principal.
- `src/models/`: definiciones de entidades de dominio.
- `src/services/`: lógica de negocio y operaciones CRUD en memoria.
- `src/ui/`: interfaz de usuario basada en consola.

### Dependencias

No hay dependencias externas obligatorias; el sistema utiliza únicamente la biblioteca estándar de Python.

## Arquitectura

El sistema sigue un patrón sencillo de separación de responsabilidades:

- `models/` contiene clases que representan los datos.
- `services/` contiene la lógica de negocio que opera sobre esas clases.
- `ui/` contiene la interacción con el usuario.
- `main.py` arma las dependencias e inicia la aplicación.

## Flujo de ejecución principal

1. `src/main.py` se ejecuta.
2. Se crea una instancia de `ValidacionesService`.
3. Se crea `ReservasService`, que depende del servicio de validaciones.
4. Se crea `ServiciosService` y `EspecialistasService`, ambos con acceso al servicio de validaciones y a las reservas.
5. Se crea `EmpleadoMenu` con referencias a los servicios.
6. Se llama a `EmpleadoMenu.mostrar_menu()`, que muestra el menú principal y permite la interacción continua.

## Interacción de usuario

Al ejecutar `python src/main.py`, el usuario ve directamente el menú principal con cuatro opciones:

1. Gestionar Servicios
2. Gestionar Especialistas
3. Gestionar Reservas
4. Salir

Cada opción abre un submenú con acciones CRUD y navegación.

## Modelos

### `src/models/especialista.py`

Clase `Especialista`:

- `cedula`: identificador único del especialista.
- `nombre`: primer nombre del especialista.
- `apellido`: apellido del especialista.
- `telefono`: teléfono de contacto.
- `email`: correo electrónico.

Métodos:

- `__init__(...)`: construye una instancia con todos los datos del especialista.
- `__str__(...)`: devuelve una representación legible para consola.
- `to_dict(...)`: serializa el especialista a un diccionario estándar.
- `from_dict(...)`: reconstruye un especialista desde un diccionario.

### `src/models/servicio.py`

Clase `Servicio`:

- `nombre`: nombre visible del servicio.
- `duracion`: duración en minutos.
- `costo`: valor monetario del servicio.
- `especialistas`: lista opcional de nombres de especialistas (no usada como asociación estricta en la lógica actual).

Métodos:

- `__init__(...)`: construye un servicio con duración y costo.
- `__str__(...)`: representa el servicio para mostrarlo en la consola.
- `to_dict(...)`: serializa el servicio a un diccionario.
- `from_dict(...)`: reconstruye un servicio desde un diccionario.

### `src/models/reserva.py`

Clase `Reserva`:

- `id`: identificador único generado automáticamente con `uuid4()` si no se proporciona.
- `cliente`: nombre del cliente que solicita la reserva.
- `servicio`: instancia de `Servicio` reservada.
- `especialista`: instancia de `Especialista` asignada.
- `fecha`: fecha de la cita (`datetime.date`).
- `hora`: hora de la cita (`datetime.time`).
- `estado`: estado de la reserva, por defecto "activa"; otras opciones posibles son "cancelada".

Métodos:

- `__init__(...)`: crea una reserva nueva con identificador único.
- `__str__(...)`: devuelve una línea descriptiva con servicio, especialista y horario.
- `to_dict(...)`: convierte la reserva y sus entidades relacionadas en diccionarios.
- `from_dict(...)`: reconstruye una reserva desde un diccionario serializado.

## Servicios de negocio

### `src/services/validaciones_service.py`

Clase `ValidacionesService`:

Responsabilidad:
- centralizar reglas de validación que afectan a reservas, especialistas y servicios.

Métodos principales:

- `validar_disponibilidad(especialista, fecha, hora, duracion_minutos, reservas, reserva_id=None)`:
  - Comprueba si un especialista ya tiene una reserva activa que se superponga con el nuevo horario.
  - Ignora la reserva actual si `reserva_id` se pasa para actualización.
  - Retorna `True` cuando el horario está libre.

- `validar_restricciones_eliminacion_especialista(cedula, reservas)`:
  - Evita eliminar a un especialista que tenga reservas futuras activas.
  - Utiliza la hora actual del sistema para comparar con las fechas de reserva.

- `validar_restricciones_eliminacion_servicio(nombre, reservas)`:
  - Evita eliminar un servicio que ya está reservado en el futuro.

- `validar_entrada_fecha(fecha_str)`:
  - Verifica el formato `YYYY-MM-DD`.

- `validar_entrada_hora(hora_str)`:
  - Verifica el formato `HH:MM`.

### `src/services/reservas_service.py`

Clase `ReservasService`:

Responsabilidad:
- gestionar la lista de reservas en memoria.
- aplicar validaciones antes de crear o actualizar reservas.

Atributos:
- `reservas`: lista de instancias `Reserva` activas o canceladas.

Métodos:

- `crear_reserva(cliente, servicio, especialista, fecha, hora)`:
  - valida la disponibilidad del especialista.
  - crea y guarda la reserva en la lista si el horario está libre.
  - retorna la reserva creada o `None` si no se puede reservar.

- `obtener_reservas()`:
  - devuelve una copia de la lista de reservas.

- `obtener_reservas_por_cliente(cliente)`:
  - filtra reservas por nombre de cliente.

- `obtener_reserva_por_id(id)`:
  - busca una reserva por su identificador único.

- `actualizar_reserva(id, nueva_fecha=None, nueva_hora=None)`:
  - actualiza fecha y hora de una reserva activa.
  - valida el nuevo horario contra otras reservas activas del mismo especialista.

- `cancelar_reserva(id)`:
  - marca la reserva como `cancelada`.

- `eliminar_reserva(id)`:
  - elimina la reserva de la lista en memoria.

- `obtener_reservas_activas_por_especialista(cedula)`:
  - devuelve las reservas activas asignadas a un especialista.

### `src/services/servicios_service.py`

Clase `ServiciosService`:

Responsabilidad:
- gestionar los servicios que se pueden reservar.

Atributos:
- `servicios`: lista en memoria de instancias `Servicio`.

Métodos:

- `crear_servicio(nombre, duracion, costo)`:
  - crea un servicio nuevo o sobrescribe uno existente con el mismo nombre.

- `obtener_servicios()`:
  - devuelve la lista de servicios.

- `obtener_servicio_por_nombre(nombre)`:
  - busca un servicio por nombre exacto.

- `actualizar_servicio(nombre, nuevo_nombre=None, duracion=None, costo=None)`:
  - modifica los atributos del servicio seleccionado.

- `eliminar_servicio(nombre)`:
  - elimina un servicio si no existe ninguna reserva futura vinculada.

### `src/services/especialistas_service.py`

Clase `EspecialistasService`:

Responsabilidad:
- gestionar a los especialistas disponibles.

Atributos:
- `especialistas`: lista en memoria de instancias `Especialista`.

Métodos:

- `crear_especialista(cedula, nombre, apellido, telefono, email)`:
  - crea un especialista o reemplaza uno existente con la misma cédula.

- `obtener_especialistas()`:
  - devuelve la lista de especialistas.

- `obtener_especialista_por_cedula(cedula)`:
  - busca un especialista por cédula.

- `actualizar_especialista(cedula, nombre=None, apellido=None, telefono=None, email=None)`:
  - actualiza los datos personales del especialista.

- `eliminar_especialista(cedula)`:
  - elimina al especialista solo si no tiene reservas futuras activas.

- `obtener_especialistas_por_servicio(servicio_nombre)`:
  - actualmente devuelve todos los especialistas, pues no existe una relación directa en la lógica actual.

## Interfaz de usuario

### `src/ui/admin_menu.py`

La clase `EmpleadoMenu` organiza el flujo de la consola y delega la lógica a los servicios.

Menú principal:
- muestra las opciones para servicios, especialistas, reservas y salir.
- la opción `Salir` termina la aplicación.

Submenú de servicios:
- `Agregar Servicio`
- `Ver Servicios`
- `Editar Servicio`
- `Eliminar Servicio`
- `Volver`

Submenú de especialistas:
- `Agregar Especialista`
- `Ver Especialistas`
- `Editar Especialista`
- `Eliminar Especialista`
- `Volver`

Submenú de reservas:
- `Crear Reserva`
- `Ver Reservas`
- `Editar Reserva`
- `Cancelar Reserva`
- `Eliminar Reserva`
- `Volver`

### Validaciones de interfaz

- Los campos obligatorios deben completarse.
- Las fechas se solicitan en formato `YYYY-MM-DD`.
- Las horas se solicitan en formato `HH:MM`.
- Las reservas solo se pueden crear cuando el especialista está disponible.
- Un servicio o especialista no se puede eliminar si existen reservas futuras activas.

## Reglas de negocio

- Una reserva se considera conflictiva si el inicio y fin de dos reservas se superponen para el mismo especialista.
- Las reservas canceladas no bloquean horarios.
- La eliminación de entidades depende de la existencia de reservas futuras activas.

## Consideraciones de implementación

- El proyecto no utiliza archivos JSON ni base de datos para persistencia.
- Los modelos incluyen métodos `to_dict()` y `from_dict()` para facilitar extensiones futuras hacia almacenamiento.
- Las rutas de importación se ajustan con `sys.path.append(...)` para permitir ejecutar `python src/main.py` desde la raíz del proyecto.
- No existe una validación específica para el campo `email`; solo se verifica que no esté vacío.

## Mejora posible

- agregar persistencia en archivos o base de datos para conservar datos entre ejecuciones.
- modelar la relación real entre `Servicio` y `Especialista` para que un especialista solo pueda reservarse en servicios compatibles.
- agregar autenticación y roles de usuario.
- mejorar la validación de datos de contacto y formatos.
- agregar pruebas automatizadas para servicios y UI.
