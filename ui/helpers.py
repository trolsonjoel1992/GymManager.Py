from datetime import date, timedelta
from services import gestor_socios

def reactivar_socio_interactivo(socio) -> bool:
    """
    Muestra información de reactivación, pide membresía a abonar según el caso,
    calcula el monto y ejecuta la reactivación si el usuario confirma.
    Retorna True si se reactivó, False si se canceló.
    """
    if socio.activo:
        print("El socio ya está activo.")
        return True

    print(f"\n--- REACTIVACIÓN DE SOCIO: {socio.nombre_completo} ---")
    print(f"DNI: {socio.dni} | Membresía actual: {socio.membresia.upper()}")

    # Determinar el caso y mostrar mensaje
    if socio.motivo_baja == "manual":
        print("\nReactivación voluntaria (baja manual).")
        print("Seleccione la membresía deseada para la reactivación:")
        print("1. Básica")
        print("2. Premium")
        opcion = input("Opción (1/2): ").strip()
        if opcion not in ("1", "2"):
            print("Opción inválida. Se mantiene la membresía actual.")
            membresia_elegida = socio.membresia
        else:
            membresia_elegida = "basica" if opcion == "1" else "premium"

    else:  # mora
        venc = gestor_socios.calcular_vencimiento(socio)
        fecha_baja = venc + timedelta(days=gestor_socios.DIAS_GRACIA)
        hoy = date.today()
        if fecha_baja.year == hoy.year and fecha_baja.month == hoy.month:
            # mismo mes
            print("\nReactivación por mora (mismo mes).")
            print(f"Debe pagar ${gestor_socios.obtener_costo_mensual(socio.membresia):.2f} (cuota del mes actual {socio.membresia.upper()}).")
            print("No hay multa porque la baja fue en el mismo mes.")
            print("No se permite cambiar de membresía en este paso; si desea cambiar, hágalo luego desde el menú de pagos.")
            membresia_elegida = socio.membresia  # forzada
        else:
            # meses diferentes
            print("\nReactivación por mora (meses diferentes).")
            multa = gestor_socios.obtener_costo_mensual(socio.membresia)
            print(f"Multa: 1 mes de {socio.membresia.upper()} (${multa:.2f})")
            print("Seleccione la membresía para la cuota del mes actual:")
            print("1. Básica")
            print("2. Premium")
            opcion = input("Opción (1/2): ").strip()
            if opcion not in ("1", "2"):
                print("Opción inválida. Se mantiene la membresía actual.")
                membresia_elegida = socio.membresia
            else:
                membresia_elegida = "basica" if opcion == "1" else "premium"

    # Obtener detalle completo
    detalle = gestor_socios.obtener_detalle_reactivacion(socio, membresia_elegida)

    # Mostrar resumen
    print(f"\nResumen de la reactivación:")
    print(f"Meses a pagar: {detalle['meses']}")
    print(f"Monto total: ${detalle['monto_total']:.2f}")
    print(f"Observación: {detalle['observacion']}")
    print(f"Fecha de cobertura: se extenderá hasta {detalle['fecha_fin'].strftime('%d/%m/%Y')}")

    # Confirmar
    confirm = input("\n¿Desea reactivar y registrar el pago? (s/n): ").strip().lower()
    if confirm != 's':
        print("Reactivación cancelada.")
        return False

    # Ejecutar reactivación
    mensaje = gestor_socios.reactivar_socio(socio.dni, detalle['meses'], detalle['membresia_elegida'])
    print(mensaje)
    return True