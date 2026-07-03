from datetime import date


def validar_numero_socio(num_str: str) -> bool:
    try:
        num = int(num_str)
        return num > 0
    except ValueError:
        return False


def validar_turno_inscripcion(turno: str) -> bool:
    return turno in ("maÃ±ana", "tarde", "noche")


def validar_fecha_inscripcion(fecha_str: str) -> bool:
    try:
        fecha = date.fromisoformat(fecha_str)
        return fecha <= date.today()
    except ValueError:
        return False