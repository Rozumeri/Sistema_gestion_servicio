classDiagram

    class Especialista {
        -cedula : String
        -nombre : String
        -apellido : String
        -telefono : String
        -email : String

        +crear()
        +editar()
        +eliminar()
    }

    class Servicio {
        -nombre : String
        -duracion : int
        -costo : float

        +crear()
        +editar()
        +eliminar()
    }

    class Reserva {
        -cliente : String
        -fecha : Date
        -hora : Time

        +crear()
        +editar()
        +cancelar()
        +consultar()
    }

    class SistemaGestion {
        +gestionarReservas()
        +gestionarServicios()
        +gestionarEspecialistas()
        +validarDisponibilidad()
    }

    Servicio "1" --> "*" Especialista : ofrecido por
    Reserva "*" --> "1" Servicio : incluye
    Reserva "*" --> "1" Especialista : asigna

    SistemaGestion --> Reserva
    SistemaGestion --> Servicio
    SistemaGestion --> Especialista