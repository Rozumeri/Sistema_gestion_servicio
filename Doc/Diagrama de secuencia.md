sequenceDiagram
    actor Cliente
    participant Sistema
    participant Servicio
    participant Especialista
    participant Reserva

    Cliente->>Sistema: Solicitar nueva reserva
    Sistema->>Servicio: Consultar servicios disponibles
    Servicio-->>Sistema: Lista de servicios

    Cliente->>Sistema: Seleccionar servicio
    Sistema->>Especialista: Consultar especialistas disponibles
    Especialista-->>Sistema: Lista de especialistas

    Cliente->>Sistema: Seleccionar especialista y horario

    Sistema->>Reserva: Validar disponibilidad
    Reserva-->>Sistema: Disponible

    Sistema->>Reserva: Crear reserva
    Reserva-->>Sistema: Reserva registrada

    Sistema-->>Cliente: Confirmación de reserva