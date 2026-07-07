from datetime import date, timedelta
from services import gestor_socios
from utils.inputs import input_choice, input_confirm

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
    if socio.motivo_baja == "manual":
        print("\nReactivación voluntaria.")
        print("Seleccione la membresía deseada para la reactivación:")
        print(f"1. Básica (${gestor_socios.COSTO_BASICA:.2f})")
        print(f"2. Premium (${gestor_socios.COSTO_PREMIUM:.2f})")
        print("3. Cancelar")
        opcion = input_choice("Opción (1/2/3): ", ["1", "2", "3"])
        if opcion == "3":
            print("Reactivación cancelada.")
            return False
        membresia_elegida = "basica" if opcion == "1" else "premium"
        detalle = gestor_socios.obtener_detalle_reactivacion(socio, membresia_elegida)
    else:  # mora
        venc = gestor_socios.calcular_vencimiento(socio)
        fecha_baja = venc + timedelta(days=gestor_socios.DIAS_GRACIA)
        hoy = date.today()
        if fecha_baja.year == hoy.year and fecha_baja.month == hoy.month:
            print("\nReactivación por cuota vencida.")
            print(
                f"Debe pagar ${gestor_socios.obtener_costo_mensual(socio.membresia):.2f} (cuota del mes actual {socio.membresia.upper()})."
            )
            print("Si desea cambiar de membresía, hágalo luego desde el menú de pagos.")
            membresia_elegida = socio.membresia
            detalle = gestor_socios.obtener_detalle_reactivacion(socio, membresia_elegida)
        else:
            print("\nReactivación por deuda acumulada.")
            print(
                f"Deuda: 1 mes de {socio.membresia.upper()} (${gestor_socios.obtener_costo_mensual(socio.membresia):.2f})"
            )
            print("Seleccione la membresía deseada para la reactivación:")
            print(f"1. Básica (${gestor_socios.COSTO_BASICA:.2f})")
            print(f"2. Premium (${gestor_socios.COSTO_PREMIUM:.2f})")
            print("3. Cancelar")
            opcion = input_choice("Opción (1/2/3): ", ["1", "2", "3"])
            if opcion == "3":
                print("Reactivación cancelada.")
                return False
            membresia_elegida = "basica" if opcion == "1" else "premium"
            detalle = gestor_socios.obtener_detalle_reactivacion(socio, membresia_elegida)
    print("\nResumen de la reactivación:")
    if detalle["meses"] == 2:
        costo_anterior = gestor_socios.obtener_costo_mensual(socio.membresia)
        costo_nuevo = gestor_socios.obtener_costo_mensual(detalle["membresia_elegida"])
        print(f"  Multa (1 mes de {socio.membresia.upper()}): ${costo_anterior:.2f}")
        print(f"  Cuota (1 mes de {detalle['membresia_elegida'].upper()}): ${costo_nuevo:.2f}")
        print(f"  TOTAL: ${detalle['monto_total']:.2f}")
        print(f"  Observación: {detalle['observacion']}")
    else:
        print(f"  Meses a pagar: {detalle['meses']}")
        print(f"  Monto total: ${detalle['monto_total']:.2f}")
        print(f"  Observación: {detalle['observacion']}")
    if not input_confirm("¿Desea reactivar y registrar el pago? (s/n): "):
        print("Reactivación cancelada.")
        return False
    mensaje = gestor_socios.reactivar_socio(socio.dni, detalle["membresia_elegida"])
    print(mensaje)
    return True