from persistence.repositorio_actividades import buscar_por_nombre
from services import gestor_actividades


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
    actividades = gestor_actividades.listar_actividades()
    if not actividades:
        print("No hay actividades disponibles.")
        return
    print("\n--- LISTADO DE ACTIVIDADES ---")
    for a in actividades:
        print(f"{a.nombre} | Horario: {a.horario} | Cupo: {a.cupo}")

def ver_detalle_actividad():
    nombre = input("Ingrese el nombre de la actividad: ").strip()
    actividad = gestor_actividades.buscar_por_nombre(nombre)
    if actividad:
        print(f"\n[DETALLE DE ACTIVIDAD]")
        print(f"Nombre: {actividad.nombre}")
        print(f"Horario: {actividad.horario}")
        print(f"Descripcion: {actividad.descripcion}")
        print(f"Cupo: {actividad.cupo}")
    else:
        print("Actividad no encontrada.")