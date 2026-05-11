# Arquitectura del Sistema de Gestión de Servicios

## Visión General

El Sistema de Gestión de Servicios es una aplicación de consola desarrollada en Python que permite a clientes y administradores gestionar reservas de servicios profesionales. El sistema es completamente modular y jerárquico, organizado en capas que separan responsabilidades claras: interfaz de usuario, lógica de negocio, modelos de datos y persistencia.

## Actores y Casos de Uso

### Actores
- **Cliente**: Usuario final que interactúa con el sistema para gestionar sus reservas personales.
- **Administrador**: Usuario con privilegios para gestionar especialistas y servicios del sistema.

### Casos de Uso Principales

#### Para Cliente:
- Ingresar Reserva: Crear una nueva reserva seleccionando servicio, especialista y horario.
- Editar Reserva: Modificar una reserva existente.
- Cancelar Reserva: Eliminar una reserva.
- Consultar Reservas: Ver reservas propias.

#### Para Administrador:
- Ingresar Especialista: Agregar nuevo especialista al sistema.
- Editar Especialista: Modificar información de especialista.
- Borrar Especialista: Eliminar especialista (con validaciones).
- Ingresar Servicio: Agregar nuevo servicio.
- Editar Servicio: Modificar información de servicio.
- Borrar Servicio: Eliminar servicio (con validaciones).
- Consultar Reservas: Ver todas las reservas del sistema.

#### Validaciones:
- Validar Disponibilidad: Verificar que el horario solicitado esté libre.
- Validar Restricciones: Comprobar reglas de negocio antes de eliminaciones.

## Arquitectura de Componentes

El sistema sigue una arquitectura modular organizada en los siguientes componentes:

### 1. Interfaz de Usuario (UI)
- **Responsabilidad**: Gestionar la interacción con el usuario a través de consola.
- **Componentes**:
  - `ConsoleUI`: Clase principal que maneja menús y navegación.
  - `ClienteMenu`: Menú específico para operaciones de cliente.
  - `AdminMenu`: Menú específico para operaciones de administrador.

### 2. Módulo de Reservas
- **Responsabilidad**: Gestionar todas las operaciones relacionadas con reservas.
- **Funciones**: Crear, editar, cancelar y consultar reservas.

### 3. Módulo de Servicios
- **Responsabilidad**: Gestionar el catálogo de servicios disponibles.
- **Funciones**: Crear, editar, eliminar y listar servicios.

### 4. Módulo de Especialistas
- **Responsabilidad**: Gestionar la información de especialistas.
- **Funciones**: Crear, editar, eliminar y listar especialistas.

### 5. Módulo de Validaciones
- **Responsabilidad**: Implementar reglas de negocio y validaciones.
- **Funciones**: Validar disponibilidad de horarios, restricciones de eliminación.

### 6. Persistencia (Base de Datos)
- **Responsabilidad**: Almacenar y recuperar datos del sistema.
- **Implementación**: Capa de abstracción para almacenamiento (inicialmente archivos JSON).

## Modelo de Datos

### Clases Principales

```python
class Especialista:
    - cedula: str
    - nombre: str
    - apellido: str
    - telefono: str
    - email: str

class Servicio:
    - nombre: str
    - duracion: int (minutos)
    - costo: float

class Reserva:
    - id: str (UUID)
    - cliente: str
    - servicio: Servicio
    - especialista: Especialista
    - fecha: date
    - hora: time
    - estado: str (activa, cancelada)
```

### Relaciones
- Un Servicio puede ser ofrecido por múltiples Especialistas (1:N)
- Una Reserva incluye un Servicio y asigna un Especialista (N:1)
- El SistemaGestion coordina todas las operaciones

## Flujo de Interacción en Consola

### Navegación Principal
```
Bienvenido al Sistema de Gestión de Servicios
===========================================
1. Ingresar como Cliente
2. Ingresar como Administrador
3. Salir

Seleccione una opción:
```

### Menú Cliente
```
Menú Cliente
============
1. Crear Reserva
2. Ver Mis Reservas
3. Editar Reserva
4. Cancelar Reserva
5. Volver al Menú Principal

Seleccione una opción:
```

### Menú Administrador
```
Menú Administrador
==================
1. Gestionar Servicios
2. Gestionar Especialistas
3. Ver Todas las Reservas
4. Volver al Menú Principal

Seleccione una opción:
```

### Ejemplo de Flujo de Creación de Reserva
1. Usuario selecciona "Crear Reserva"
2. Sistema muestra lista de servicios disponibles
3. Usuario selecciona servicio
4. Sistema muestra especialistas disponibles para ese servicio
5. Usuario selecciona especialista
6. Sistema solicita fecha y hora
7. Sistema valida disponibilidad
8. Si disponible: crea reserva y muestra confirmación
9. Si no disponible: muestra mensaje de error y permite reintentar

## Jerarquía de Módulos Python

```
src/
├── __init__.py
├── main.py                    # Punto de entrada del sistema
├── models/
│   ├── __init__.py
│   ├── especialista.py        # Clase Especialista
│   ├── servicio.py            # Clase Servicio
│   └── reserva.py             # Clase Reserva
├── services/
│   ├── __init__.py
│   ├── reservas_service.py    # Lógica de negocio para reservas
│   ├── servicios_service.py   # Lógica de negocio para servicios
│   ├── especialistas_service.py # Lógica de negocio para especialistas
│   └── validaciones_service.py # Validaciones de negocio
├── persistence/
│   ├── __init__.py
│   ├── database.py            # Interfaz de base de datos
│   └── json_storage.py        # Implementación JSON
└── ui/
    ├── __init__.py
    ├── console_ui.py          # Interfaz principal de consola
    ├── cliente_menu.py        # Menú cliente
    └── admin_menu.py          # Menú administrador
```

## Dependencias y Tecnologías

- **Lenguaje**: Python 3.8+
- **Persistencia**: Archivos JSON (extensible a bases de datos SQL/NoSQL)
- **Validaciones**: Lógica de negocio integrada
- **Interfaz**: Consola interactiva con menús

## Extensibilidad

La arquitectura modular permite:
- Cambiar la interfaz de usuario (consola → web → GUI)
- Cambiar el mecanismo de persistencia (JSON → SQLite → PostgreSQL)
- Agregar nuevos tipos de validaciones
- Extender funcionalidades sin afectar otros módulos

## Seguridad y Validaciones

- Validación de entrada de usuario
- Verificación de permisos (cliente vs administrador)
- Validaciones de negocio antes de operaciones críticas
- Manejo de errores y excepciones