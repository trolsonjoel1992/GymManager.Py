def validar_id_actividad(id_str: str) -> bool:
    """Valida que sea un número entero positivo."""
    try:
        num = int(id_str)
        return num > 0
    except ValueError:
        return False


def validar_nombre_actividad(nombre: str) -> bool:
    """Nombre no vacío y razonable (sin caracteres extraños)."""
    return bool(nombre.strip() and len(nombre) >= 3)


def validar_cupo(cupo_str: str) -> bool:
    """Valida que sea un número entero no negativo."""
    try:
        num = int(cupo_str)
        return num >= 0
    except ValueError:
        return False


def validar_turno(turno: str) -> bool:
    """Valida que el turno sea 'mañana', 'tarde' o 'noche'."""
    return turno in ("mañana", "tarde", "noche")


def validar_turnos_lista(turnos_str: str) -> bool:
    """
    Valida una lista de turnos separados por comas.
    Ej: "mañana,tarde" -> True
    """
    if not turnos_str:
        return False
    turnos = [t.strip() for t in turnos_str.split(",")]
    if not turnos:
        return False
    for t in turnos:
        if not validar_turno(t):
            return False
    return True