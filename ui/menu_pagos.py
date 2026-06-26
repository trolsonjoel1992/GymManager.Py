from services import gestor_pagos
from services import gestor_socios
from ui.helpers import reactivar_socio_interactivo
from utils.inputs import solicitar_dato

def mostrar_submenu():
    while True:
        print("\n--- PAGOS Y CONTROL DE MOROSIDAD ---")
        print("1. Registrar pago")
        print("2. Cambiar membresía a Premium")
        print("3. Ver estado de cuotas de un socio")
        print("4. Ver historial de pagos de un socio")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_pago_interactivo()
        elif opcion == "2":
            cambiar_membresia_premium()
        elif opcion == "3":
            ver_estado_cuotas()
        elif opcion == "4":
            ver_historial_pagos()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def registrar_pago_interactivo():
    identificador = input("DNI o número de socio: ").strip()
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return

    if not socio.activo:
        print("El socio está inactivo. Para registrar un pago, primero debe reactivarlo.")
        print("¿Desea reactivarlo o cancelar?")
        print("1. Reactivar")
        print("2. Cancelar")
        opcion = input("Opción (1/2): ").strip()
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

    # Solicitar membresía a abonar
    print("\nSeleccione la membresía que abona:")
    print(f"1. Básica (${gestor_socios.COSTO_BASICA:.2f})")
    print(f"2. Premium (${gestor_socios.COSTO_PREMIUM:.2f})")
    print("3. Cancelar")
    while True:
        opcion_memb = input("Opción (1/2/3): ").strip()
        if opcion_memb == "3":
            print("Operación cancelada.")
            return
        if opcion_memb in ("1", "2"):
            break
        print("Opción inválida. Intente nuevamente.")
    membresia_elegida = "basica" if opcion_memb == "1" else "premium"

    # Solicitar cantidad de meses
    try:
        meses = int(input("Cantidad de meses (1,2,3...): ").strip())
        if meses < 1:
            print("Debe ser al menos 1.")
            return
    except ValueError:
        print("Número inválido.")
        return

    costo_mensual = gestor_socios.obtener_costo_mensual(membresia_elegida)
    monto = costo_mensual * meses

    nueva_membresia = membresia_elegida if membresia_elegida != socio.membresia else None

    mensaje = gestor_pagos.registrar_pago(socio.dni, monto, meses, nueva_membresia)
    print(mensaje)

def cambiar_membresia_premium():
    """Upgrade de Básica a Premium con pago de 1 mes."""
    identificador = input("DNI o número de socio: ").strip()
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
    print(f"Membresía actual: BÁSICA")
    confirm = input("¿Desea cambiar a membresía PREMIUM? El costo es de 1 mes de Premium ($50.00). (s/n): ").strip().lower()
    if confirm != 's':
        print("Cambio cancelado.")
        return

    costo_premium = gestor_socios.obtener_costo_mensual("premium")
    monto = costo_premium
    meses = 1

    mensaje = gestor_pagos.registrar_pago(socio.dni, monto, meses, nueva_membresia="premium")
    print(mensaje)

def ver_estado_cuotas():
    identificador = input("DNI o número de socio: ").strip()
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    mensaje = gestor_pagos.obtener_estado_cuotas(socio.dni, tipo_busqueda="dni")
    print(mensaje)

def ver_historial_pagos():
    identificador = input("DNI o número de socio: ").strip()
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
        print(f"Fecha: {p.fecha_pago} | Monto: ${p.monto} | Meses: {p.meses_cubiertos} | Membresía: {p.membresia.upper()} | {p.observaciones}")