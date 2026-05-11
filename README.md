# Sistema de Gestión de Servicios

Una aplicación de consola modular y jerárquica desarrollada en Python para la gestión de reservas de servicios profesionales. Permite a clientes crear y gestionar reservas, mientras que administradores pueden gestionar especialistas y servicios.

## Descripción

El Sistema de Gestión de Servicios facilita la coordinación entre clientes que necesitan servicios profesionales y especialistas que los ofrecen. Los clientes pueden reservar servicios en horarios disponibles, mientras que los administradores mantienen actualizado el catálogo de servicios y especialistas.

### Características Principales
- **Gestión de Reservas**: Crear, editar, cancelar y consultar reservas
- **Catálogo de Servicios**: Administración completa de servicios disponibles
- **Gestión de Especialistas**: Control de información de profesionales
- **Validaciones Automáticas**: Verificación de disponibilidad y restricciones
- **Interfaz de Consola**: Navegación intuitiva con menús interactivos
- **Arquitectura Modular**: Diseño jerárquico extensible y mantenible

## Arquitectura

El sistema sigue una arquitectura modular organizada en capas:

- **UI (Interfaz de Usuario)**: Maneja la interacción por consola
- **Services (Servicios de Negocio)**: Contiene la lógica de negocio
- **Models (Modelos)**: Define las entidades del dominio
- **Persistence (Persistencia)**: Abstrae el almacenamiento de datos

Para más detalles, consulta [`Doc/Arquitectura del Sistema.md`](Doc/Arquitectura del Sistema.md).

## Requisitos del Sistema

- **Python**: Versión 3.8 o superior
- **Dependencias**: Ninguna externa (usa solo librerías estándar de Python)
- **Sistema Operativo**: Compatible con Windows, macOS y Linux

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Rozumeri/Sistema_gestion_servicio.git
cd Sistema_gestion_servicio
```

### 2. Verificar Python
```bash
python --version  # Debe ser 3.8+
```

### 3. (Opcional) Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

*Nota: Actualmente no hay dependencias externas, pero el archivo `requirements.txt` está preparado para futuras extensiones.*

## Despliegue y Ejecución

### Ejecución Básica
```bash
python src/main.py
```

### Ejecución con Entorno Virtual
```bash
source venv/bin/activate
python src/main.py
```

### Inicialización de Datos de Ejemplo (Opcional)
Para poblar el sistema con datos de prueba:
```bash
python src/inicializar_datos.py
```

Esto creará servicios, especialistas y algunas reservas de ejemplo.

## Uso del Sistema

### Navegación Principal
Al iniciar el sistema, verás el menú principal:

```
Bienvenido al Sistema de Gestión de Servicios
===========================================
1. Ingresar como Cliente
2. Ingresar como Administrador
3. Salir

Seleccione una opción:
```

### Como Cliente

#### Crear una Reserva
1. Selecciona "1. Ingresar como Cliente"
2. Elige "1. Crear Reserva"
3. Sigue los pasos:
   - Selecciona un servicio de la lista
   - Elige un especialista disponible
   - Ingresa fecha (YYYY-MM-DD)
   - Ingresa hora (HH:MM)
4. El sistema valida la disponibilidad automáticamente
5. Si está disponible, confirma la reserva

#### Gestionar Reservas Existentes
- **Ver Reservas**: Opción 2 del menú cliente
- **Editar Reserva**: Opción 3 (modificar fecha/hora)
- **Cancelar Reserva**: Opción 4

### Como Administrador

#### Gestionar Servicios
1. Selecciona "2. Ingresar como Administrador"
2. Elige "1. Gestionar Servicios"
3. Operaciones disponibles:
   - Agregar nuevo servicio
   - Editar servicio existente
   - Eliminar servicio
   - Listar todos los servicios

#### Gestionar Especialistas
- Opción "2. Gestionar Especialistas"
- Operaciones similares: agregar, editar, eliminar, listar

#### Ver Todas las Reservas
- Opción "3. Ver Todas las Reservas"
- Vista completa de todas las reservas del sistema

### Comandos de Navegación
- Usa números para seleccionar opciones
- Presiona Enter para confirmar selecciones
- Escribe "volver" o "0" en algunos menús para regresar
- El sistema valida todas las entradas automáticamente

## Estructura del Proyecto

```
Sistema_gestion_servicio/
├── README.md
├── requirements.txt
├── Doc/
│   ├── Arquitectura del Sistema.md
│   ├── Diagrama casos de uso.md
│   ├── Diagrama de actividades.md
│   ├── Diagrama de clases.md
│   ├── Diagrama de componentes.md
│   └── Diagrama de secuencia.md
└── src/
    ├── main.py
    ├── models/
    │   ├── __init__.py
    │   ├── especialista.py
    │   ├── servicio.py
    │   └── reserva.py
    ├── services/
    │   ├── __init__.py
    │   ├── reservas_service.py
    │   ├── servicios_service.py
    │   ├── especialistas_service.py
    │   └── validaciones_service.py
    ├── persistence/
    │   ├── __init__.py
    │   ├── database.py
    │   └── json_storage.py
    └── ui/
        ├── __init__.py
        ├── console_ui.py
        ├── cliente_menu.py
        └── admin_menu.py
```

## Desarrollo y Extensibilidad

### Agregar Nuevos Servicios
1. Implementa la lógica en `services/`
2. Actualiza los menús en `ui/`
3. Agrega validaciones en `validaciones_service.py`

### Cambiar Persistencia
1. Implementa nueva clase en `persistence/`
2. Actualiza `database.py` para usar la nueva implementación
3. No requiere cambios en otras capas

### Testing
```bash
# Ejecutar tests (cuando se implementen)
python -m pytest tests/
```

## Solución de Problemas

### Error de Python Version
- Asegúrate de tener Python 3.8+ instalado
- Verifica con `python --version`

### Problemas de Permisos
- En Linux/macOS: `chmod +x src/main.py`
- Ejecuta con permisos de administrador si es necesario

### Datos No Persisten
- Verifica permisos de escritura en el directorio
- Los datos se almacenan en archivos JSON en `data/`

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Guías de Contribución
- Sigue la arquitectura modular existente
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario
- Mantén compatibilidad con Python 3.8+

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:
- Abre un issue en GitHub
- Revisa la documentación en `Doc/`
- Consulta los diagramas de arquitectura para entender el flujo del sistema