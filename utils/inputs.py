def solicitar_dato(mensaje, validador=None, mensaje_error="Dato inválido", permitir_vacio=False):
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