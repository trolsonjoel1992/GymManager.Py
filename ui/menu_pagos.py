from services import gestor_pagos
from services import gestor_socios
from ui.helpers import reactivar_socio_interactivo
from utils.inputs import solicitar_dato

def mostrar_submenu():
    while True:
        print("\n--- PAGOS Y CONTROL DE MOROSIDAD ---")
        print("1. Registrar pago")
        print("2. Ver estado de cuotas de un socio")
        print("3. Ver historial de pagos de un socio")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_pago_interactivo()
        elif opcion == "2":
            ver_estado_cuotas()
        elif opcion == "3":
            ver_historial_pagos()
        elif opcion == "4":
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
        print("¿Desea reactivarlo ahora?")
        reactivado = reactivar_socio_interactivo(socio)
        if reactivado:
            print("La reactivación ya incluyó el pago correspondiente. Operación finalizada.")
        else:
            print("Registro de pago cancelado.")
        return

    try:
        monto = float(input("Monto pagado: "))
    except ValueError:
        print("Monto inválido.")
        return
    meses = 1
    while True:
        entrada = input("Cantidad de meses que paga (1,2,3...): ").strip()
        if entrada == "":
            meses = 1
            break
        try:
            meses = int(entrada)
            if meses >= 1:
                break
            else:
                print("Debe ser al menos 1.")
        except ValueError:
            print("Ingrese un número entero.")

    nueva_membresia = None
    if socio.membresia == "basica":
        cambio = input("¿Desea cambiar a membresía Premium a partir del próximo mes? (s/n): ").strip().lower()
        if cambio == 's':
            nueva_membresia = "premium"
            costo_premium = gestor_socios.obtener_costo_mensual("premium")
            print(f"Nota: El costo mensual Premium es ${costo_premium:.2f}. Asegúrese de ingresar el monto correcto.")
    else:
        print("El socio ya tiene membresía Premium.")

    mensaje = gestor_pagos.registrar_pago(socio.dni, monto, meses, nueva_membresia)
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