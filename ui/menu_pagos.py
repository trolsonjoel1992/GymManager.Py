def mostrar_submenu():
    while True:
        print("\n--- PAGOS Y CONTROL DE MOROSIDAD ---")
        print("1. Registrar pago de cuota")
        print("2. Ver estado de cuotas de un socio")
        print("3. Listar socios morosos")
        print("4. Cambiar estado de moroso a activo (manual)")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_pago()
        elif opcion == "2":
            ver_estado_cuotas()
        elif opcion == "3":
            listar_morosos()
        elif opcion == "4":
            cambiar_estado()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def registrar_pago():
    dni = input("DNI del socio: ")
    monto = input("Monto pagado: ")
    print(f"→ Pago de ${monto} registrado para socio {dni} (simulación).")

def ver_estado_cuotas():
    dni = input("DNI del socio: ")
    print(f"\n[Estado de cuotas de {dni}] (Funcionalidad en desarrollo)")

def listar_morosos():
    print("\n[LISTA DE MOROSOS] (Funcionalidad en desarrollo)")

def cambiar_estado():
    dni = input("DNI del socio: ")
    print(f"→ Estado de socio {dni} cambiado a 'Activo' (simulación).")