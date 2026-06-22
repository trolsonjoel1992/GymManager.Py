# ui/menu_pagos.py
from services import gestor_pagos
from services import gestor_socios

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
    dni = input("DNI del socio: ").strip()
    try:
        monto = float(input("Monto pagado: "))
        meses = int(input("Cantidad de meses que paga (1,2,3...): ") or "1")
    except ValueError:
        print("Dato inválido.")
        return
    mensaje = gestor_pagos.registrar_pago(dni, monto, meses)
    print(mensaje)

def ver_estado_cuotas():
    dni = input("DNI del socio: ").strip()
    mensaje = gestor_pagos.mostrar_estado_cuotas(dni)
    print(mensaje)

def ver_historial_pagos():
    dni = input("DNI del socio: ").strip()
    pagos = gestor_pagos.obtener_historial_pagos(dni)
    if not pagos:
        print("No hay pagos registrados para este socio.")
        return
    print(f"\n--- HISTORIAL DE PAGOS DE {dni} ---")
    for p in pagos:
        print(f"Fecha: {p.fecha_pago} | Monto: ${p.monto} | Meses: {p.meses_cubiertos} | {p.observaciones}")