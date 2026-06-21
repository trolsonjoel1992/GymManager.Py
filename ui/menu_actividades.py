def mostrar_submenu():
    while True:
        print("\n--- GESTIÓN DE ACTIVIDADES (predefinidas) ---")
        print("1. Ver listado de actividades disponibles")
        print("2. Ver detalles de una actividad")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            listar_actividades()
        elif opcion == "2":
            ver_detalle_actividad()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

def listar_actividades():
    print("\n[LISTADO DE ACTIVIDADES]")
    # Hardcode temporal (luego se cargará desde archivo)
    actividades = [
        {"id": 1, "nombre": "Yoga", "horario": "Lun y Mié 18:00", "cupo": 15},
        {"id": 2, "nombre": "Spinning", "horario": "Mar y Jue 19:00", "cupo": 20},
        {"id": 3, "nombre": "Pilates", "horario": "Lun a Vie 17:00", "cupo": 12},
        {"id": 4, "nombre": "Musculación", "horario": "Horario libre", "cupo": None},
    ]
    for act in actividades:
        cupo_str = f"Cupo: {act['cupo']}" if act['cupo'] else "Sin cupo"
        print(f"ID: {act['id']} | {act['nombre']} | {act['horario']} | {cupo_str}")

def ver_detalle_actividad():
    id_act = input("Ingrese ID de la actividad: ")
    print(f"\n[Detalles de actividad {id_act}] (Funcionalidad en desarrollo)")