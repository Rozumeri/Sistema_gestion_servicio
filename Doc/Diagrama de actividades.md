flowchart TD

    A([Inicio]) --> B[Seleccionar servicio]
    B --> C[Consultar especialistas disponibles]
    C --> D[Seleccionar especialista]
    D --> E[Seleccionar fecha y hora]

    E --> F{Horario disponible?}

    F -- No --> G[Mostrar mensaje de conflicto]
    G --> E

    F -- Sí --> H[Registrar reserva]
    H --> I[Mostrar confirmación]

    I --> J([Fin])