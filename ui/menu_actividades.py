from persistence import repositorio_inscripciones
from services import gestor_actividades
from utils.inputs import input_int, input_str

def mostrar_submenu():
    while True:
        print("\n--- GESTIÓN DE ACTIVIDADES ---")
        print("1. Ver listado de actividades disponibles")
        print("2. Ver detalles de una actividad")
        print("3. Volver al menú principal")
        opcion = input_int("Seleccione opción: ", min=1, max=3)
        if opcion == 1:
            listar_disponibles()
        elif opcion == 2:
            ver_detalle()
        elif opcion == 3:
            break

def listar_disponibles():
    disponibles = gestor_actividades.listar_actividades_disponibles()
    if not disponibles:
        print("No hay actividades disponibles en este momento.")
        return
    print("\nActividades disponibles:")
    for act in disponibles:
        turnos = ", ".join(act["turnos_disponibles"])
        print(f"ID: {act['id']} | {act['nombre']} | Turnos con cupo: {turnos}")

def ver_detalle():
    identificador = input_str("Ingrese número o nombre de la actividad: ").strip()
    if not identificador:
        print("Debe ingresar un valor.")
        return
    act = None
    if identificador.isdigit():
        act = gestor_actividades.obtener_actividad(int(identificador))
    else:
        act = gestor_actividades.obtener_actividad_por_nombre(identificador)
    if not act:
        print("Actividad no encontrada.")
        return
    print(f"\n--- {act.nombre} ---")
    print(f"Descripción: {act.descripcion}")
    print("Cupos por turno:")
    for turno in act.turnos:
        cupo = act.cupo_por_turno(turno)
        inscritos = repositorio_inscripciones.contar_inscritos_activos(act.id, turno)
        print(f"  {turno.capitalize()}: {inscritos}/{cupo}")
    print(f"Estado: {'Activa' if act.activa else 'Inactiva'}")