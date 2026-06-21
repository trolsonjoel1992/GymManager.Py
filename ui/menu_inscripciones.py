def mostrar_submenu():
    while True:
        print("\n--- INSCRIPCIONES A ACTIVIDADES ---")
        print("1. Inscribir socio a una actividad")
        print("2. Ver actividades de un socio")
        print("3. Dar de baja a un socio de una actividad")
        print("4. Ver listado de socios inscritos en una actividad")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            inscribir_socio()
        elif opcion == "2":
            ver_actividades_socio()
        elif opcion == "3":
            dar_baja_socio()
        elif opcion == "4":
            ver_socios_por_actividad()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def inscribir_socio():
    print("\n[INSCRIBIR SOCIO] (Funcionalidad en desarrollo)")
    dni = input("DNI del socio: ")
    id_act = input("ID de la actividad: ")
    print(f"→ Inscripción de socio {dni} a actividad {id_act} registrada (simulación).")

def ver_actividades_socio():
    dni = input("DNI del socio: ")
    print(f"\n[Actividades del socio {dni}] (Funcionalidad en desarrollo)")

def dar_baja_socio():
    dni = input("DNI del socio: ")
    id_act = input("ID de la actividad: ")
    print(f"→ Baja de socio {dni} de actividad {id_act} (simulación).")

def ver_socios_por_actividad():
    id_act = input("ID de la actividad: ")
    print(f"\n[Lista de socios en actividad {id_act}] (Funcionalidad en desarrollo)")