flowchart LR

    Usuario[Usuario / Cliente]

    subgraph Frontend
        UI[Interfaz del Sistema]
    end

    subgraph Backend
        RS[Modulo Reservas]
        SS[Modulo Servicios]
        ES[Modulo Especialistas]
        VS[Modulo Validaciones]
    end

    subgraph BaseDatos
        DB[(Base de Datos)]
    end

    Usuario --> UI

    UI --> RS
    UI --> SS
    UI --> ES

    RS --> VS
    RS --> DB

    SS --> DB
    ES --> DB

    VS --> DB