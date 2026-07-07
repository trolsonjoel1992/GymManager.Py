from services import gestor_pagos, gestor_socios
from ui.helpers import reactivar_socio_interactivo
from utils.inputs import input_choice, input_confirm, input_int, input_str


def mostrar_submenu():
    while True:
        print("\n--- PAGOS Y CONTROL DE MOROSIDAD ---")
        print("1. Registrar pago")
        print("2. Cambiar membresía a Premium")
        print("3. Ver estado de cuotas de un socio")
        print("4. Ver historial de pagos de un socio")
        print("5. Volver al menú principal")
        opcion = input_int("Seleccione una opción: ", min=1, max=5)
        if opcion == 1:
            registrar_pago_interactivo()
        elif opcion == 2:
            cambiar_membresia_premium()
        elif opcion == 3:
            ver_estado_cuotas()
        elif opcion == 4:
            ver_historial_pagos()
        elif opcion == 5:
            break


def registrar_pago_interactivo():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return

    if not socio.activo:
        print("El socio está inactivo. Para registrar un pago, primero debe reactivarlo.")
        print("¿Desea reactivarlo o cancelar?")
        print("1. Reactivar")
        print("2. Cancelar")
        opcion = input_choice("Opción (1/2): ", ["1", "2"])
        if opcion == "1":
            if reactivar_socio_interactivo(socio):
                print("Reactivación completada. El pago se registró durante la reactivación.")
            else:
                print("Reactivación cancelada.")
        else:
            print("Operación cancelada.")
        return

    print(f"\nSocio: {socio.nombre_completo} (DNI: {socio.dni})")
    print(f"Membresía actual: {socio.membresia.upper()}")

    print("\nSeleccione la membresía que abona:")
    print(f"1. Básica (${gestor_socios.COSTO_BASICA:.2f})")
    print(f"2. Premium (${gestor_socios.COSTO_PREMIUM:.2f})")
    print("3. Cancelar")
    opcion_memb = input_choice("Opción (1/2/3): ", ["1", "2", "3"])
    if opcion_memb == "3":
        print("Operación cancelada.")
        return
    membresia_elegida = "basica" if opcion_memb == "1" else "premium"

    meses = input_int("Cantidad de meses (1,2,3...): ", min=1)

    costo_mensual = gestor_socios.obtener_costo_mensual(membresia_elegida)
    monto = costo_mensual * meses

    nueva_membresia = membresia_elegida if membresia_elegida != socio.membresia else None

    mensaje = gestor_pagos.registrar_pago(socio.dni, monto, meses, nueva_membresia)
    print(mensaje)


def cambiar_membresia_premium():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return

    if not socio.activo:
        print("El socio está inactivo. Debe reactivarlo primero.")
        return

    if socio.membresia == "premium":
        print("El socio ya tiene membresía Premium.")
        return

    print(f"\nSocio: {socio.nombre_completo} (DNI: {socio.dni})")
    print("Membresía actual: BÁSICA")
    if not input_confirm(
        "¿Desea cambiar a membresía PREMIUM? El costo es de 1 mes de Premium ($50.00). (s/n): "
    ):
        print("Cambio cancelado.")
        return

    costo_premium = gestor_socios.obtener_costo_mensual("premium")
    monto = costo_premium
    meses = 1

    mensaje = gestor_pagos.registrar_pago(socio.dni, monto, meses, nueva_membresia="premium")
    print(mensaje)


def ver_estado_cuotas():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    mensaje = gestor_pagos.obtener_estado_cuotas(socio.dni, tipo_busqueda="dni")
    print(mensaje)


def ver_historial_pagos():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    pagos = gestor_pagos.obtener_historial_pagos(str(socio.numero_socio), tipo_busqueda="numero")
    if not pagos:
        print("No hay pagos registrados para este socio.")
        return
    print(f"\n--- HISTORIAL DE PAGOS DE {socio.nombre_completo} ---")
    for p in pagos:
        print(
            f"Fecha: {p.fecha_pago} | Monto: ${p.monto} | Meses: {p.meses_cubiertos} | Membresía: {p.membresia.upper()} | {p.observaciones}"
        )
