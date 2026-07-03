from datetime import date

def solicitar_dato(mensaje, validador=None, mensaje_error="Dato inválido", permitir_vacio=False):
    """
    Solicita un dato al usuario, con validación opcional.
    - validador: función que recibe str y retorna bool.
    - permitir_vacio: si True, permite ingresar cadena vacía (retorna None).
    """
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and valor == "":
            return None
        if validador is None:
            if valor:
                return valor
            print("Este campo no puede estar vacío.")
            continue
        if validador(valor):
            return valor
        print(mensaje_error)

def input_str(mensaje, permitir_vacio=False):
    """Solicita una cadena, opcionalmente vacía."""
    return solicitar_dato(mensaje, permitir_vacio=permitir_vacio)

def input_int(mensaje, min=None, max=None):
    """Solicita un entero, opcionalmente con rango."""
    def validador_int(valor):
        try:
            num = int(valor)
            if min is not None and num < min:
                return False
            if max is not None and num > max:
                return False
            return True
        except ValueError:
            return False
    mensaje_error = "Debe ingresar un número entero válido."
    if min is not None and max is not None:
        mensaje_error += f" (entre {min} y {max})"
    elif min is not None:
        mensaje_error += f" (mayor o igual a {min})"
    elif max is not None:
        mensaje_error += f" (menor o igual a {max})"
    valor_str = solicitar_dato(mensaje, validador_int, mensaje_error)
    return int(valor_str)

def input_date(mensaje, permitir_vacio=False):
    """Solicita fecha en formato YYYY-MM-DD, opcionalmente vacía."""
    def validador_fecha(valor):
        try:
            date.fromisoformat(valor)
            return True
        except ValueError:
            return False
    return solicitar_dato(
        mensaje,
        validador_fecha,
        "Formato inválido. Use AAAA-MM-DD (ej: 2026-06-11)",
        permitir_vacio,
    )

def input_confirm(mensaje):
    """Solicita confirmación s/n, retorna True para 's'."""
    def validador_sn(valor):
        return valor.lower() in ("s", "n")
    respuesta = solicitar_dato(mensaje, validador_sn, "Responda 's' para sí o 'n' para no.")
    return respuesta.lower() == "s"

def input_choice(mensaje, opciones):
    """Solicita una opción de una lista de opciones (strings)."""
    def validador_opcion(valor):
        return valor in opciones
    return solicitar_dato(
        mensaje, validador_opcion, f"Opción no válida. Las opciones son: {', '.join(opciones)}"
    )