from services import gestor_socios

def reactivar_socio_interactivo(socio) -> bool:
    """
    Muestra la información de reactivación con costos, permite cambiar membresía,
    y si el usuario confirma, ejecuta la reactivación.
    Retorna True si se reactivó, False si se canceló.
    """
    if socio.activo:
        print("El socio ya está activo.")
        return True

    print(f"\n--- REACTIVACIÓN DE SOCIO: {socio.nombre_completo} ---")
    print(f"Membresía actual: {socio.membresia.upper()}")
    print("¿Desea cambiar la membresía?")
    opcion = input("1. Mantener actual\n2. Cambiar a Básica\n3. Cambiar a Premium\nOpción: ").strip()
    nueva_membresia = None
    if opcion == "2":
        nueva_membresia = "basica"
    elif opcion == "3":
        nueva_membresia = "premium"
    # si opción inválida o "1", se mantiene la actual

    meses_a_pagar = gestor_socios.calcular_meses_reactivacion(socio)
    membresia_para_pago = nueva_membresia if nueva_membresia else socio.membresia
    costo_mensual = gestor_socios.obtener_costo_mensual(membresia_para_pago)
    monto_total = costo_mensual * meses_a_pagar

    print(f"\nMeses a pagar: {meses_a_pagar}")
    print(f"Costo por mes: ${costo_mensual:.2f}")
    print(f"Monto total: ${monto_total:.2f}")
    if meses_a_pagar == 1:
        print("Se extiende la cobertura por 1 mes.")
    else:
        print("Se pagan 2 meses (mes vencido + mes actual), pero la cobertura se extiende solo 1 mes (el segundo mes es multa).")

    confirm = input("\n¿Desea reactivar y registrar el pago? (s/n): ").strip().lower()
    if confirm == 's':
        mensaje = gestor_socios.reactivar_socio(socio.dni, meses_a_pagar, nueva_membresia)
        print(mensaje)
        return True
    else:
        print("Reactivación cancelada.")
        return False