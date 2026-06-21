def mostrar_submenu():
    while True:
        print("\n--- CONTROL DE ASISTENCIA ---")
        print("1. Marcar asistencia individual")
        print("2. Marcar asistencia masiva (por actividad)")
        print("3. Ver historial de asistencias de un socio")
        print("4. Ver asistencias de una actividad (rango de fechas)")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            marcar_asistencia_individual()
        elif opcion == "2":
            marcar_asistencia_masiva()
        elif opcion == "3":
            historial_socio()
        elif opcion == "4":
            asistencias_actividad()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def marcar_asistencia_individual():
    dni = input("DNI del socio: ")
    id_act = input("ID de la actividad: ")
    print(f"→ Asistencia registrada para socio {dni} en actividad {id_act} (simulación).")

def marcar_asistencia_masiva():
    id_act = input("ID de la actividad: ")
    print(f"→ Asistencia masiva para actividad {id_act} (simulación).")

def historial_socio():
    dni = input("DNI del socio: ")
    print(f"\n[Historial de asistencias de {dni}] (Funcionalidad en desarrollo)")

def asistencias_actividad():
    id_act = input("ID de la actividad: ")
    fecha_ini = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    print(f"\n[Asistencias de actividad {id_act} entre {fecha_ini} y {fecha_fin}] (Funcionalidad en desarrollo)")