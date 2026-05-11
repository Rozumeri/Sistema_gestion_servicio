flowchart LR
    Cliente([Cliente])
    Admin([Administrador])

    subgraph Sistema["Sistema de Gestión de Servicios"]
        UC1((Ingresar Reserva))
        UC2((Editar Reserva))
        UC3((Cancelar Reserva))
        UC4((Consultar Reservas))

        UC5((Ingresar Especialista))
        UC6((Editar Especialista))
        UC7((Borrar Especialista))

        UC8((Ingresar Servicio))
        UC9((Editar Servicio))
        UC10((Borrar Servicio))

        UC11((Validar Disponibilidad))
        UC12((Validar Restricciones))
    end

    Cliente --> UC1
    Cliente --> UC2
    Cliente --> UC3
    Cliente --> UC4

    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC4

    UC1 --> UC11
    UC2 --> UC11

    UC7 --> UC12
    UC10 --> UC12