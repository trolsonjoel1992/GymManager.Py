from datetime import date
from services import gestor_actividades, gestor_inscripciones, gestor_socios
from utils.inputs import input_int, input_str

ID_MUSCULACION = gestor_actividades.ID_MUSCULACION

def mostrar_submenu():
    while True:
        print("\n--- GESTIÓN DE INSCRIPCIONES ---")
        print("1. Inscribir socio a una actividad")
        print("2. Dar de baja a un socio de una actividad")
        print("3. Ver actividades de un socio")
        print("4. Ver listado de socios inscritos en una actividad")
        print("5. Volver al menú principal")
        opcion = input_int("Seleccione opción: ", min=1, max=5)
        if opcion == 1:
            inscribir()
        elif opcion == 2:
            dar_baja()
        elif opcion == 3:
            ver_actividades_socio()
        elif opcion == 4:
            ver_socios_actividad()
        elif opcion == 5:
            break

def inscribir():
    identificador = input_str("Ingrese DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    if not socio.activo:
        print("El socio está inactivo. No puede inscribirse.")
        return
    estado = gestor_socios.obtener_estado(socio)
    if estado == "debe_cuota":
        print("El socio está en período de gracia (mora). Debe regularizar su cuota antes de inscribirse.")
        return
    disponibles = gestor_actividades.listar_actividades_disponibles()
    if not disponibles:
        print("No hay actividades con cupo disponible.")
        return
    print("\nActividades disponibles:")
    for idx, act in enumerate(disponibles, 1):
        print(f"{idx}. {act['nombre']} (ID: {act['id']})")
    print(f"{len(disponibles)+1}. Cancelar")
    opcion = input_int("Seleccione una actividad: ", min=1, max=len(disponibles) + 1)
    if opcion == len(disponibles) + 1:
        print("Operación cancelada.")
        return
    act_seleccionada = disponibles[opcion - 1]
    id_act = act_seleccionada["id"]
    turnos = act_seleccionada["turnos_disponibles"]
    print("\nTurnos disponibles:")
    for idx, turno in enumerate(turnos, 1):
        print(f"{idx}. {turno.capitalize()}")
    print(f"{len(turnos)+1}. Cancelar")
    opcion_turno = input_int("Seleccione un turno: ", min=1, max=len(turnos) + 1)
    if opcion_turno == len(turnos) + 1:
        print("Operación cancelada.")
        return
    turno_elegido = turnos[opcion_turno - 1]
    resultado = gestor_inscripciones.inscribir_socio(socio.numero_socio, id_act, turno_elegido)
    print(resultado)

def dar_baja():
    identificador = input_str("Ingrese DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    inscripciones = gestor_inscripciones.listar_actividades_de_socio(socio.numero_socio)
    hoy = date.today()
    activas = [i for i in inscripciones if i.activa and i.fecha_fin >= hoy]
    if not activas:
        print("El socio no tiene inscripciones activas.")
        return
    print("\nInscripciones activas:")
    for idx, ins in enumerate(activas, 1):
        act = gestor_actividades.obtener_actividad(ins.id_actividad)
        nombre = act.nombre if act else "Desconocida"
        print(f"{idx}. {nombre} - Turno: {ins.turno.capitalize()} (hasta {ins.fecha_fin.strftime('%Y-%m-%d')})")
    print(f"{len(activas)+1}. Cancelar")
    opcion = input_int("Seleccione la inscripción a dar de baja: ", min=1, max=len(activas) + 1)
    if opcion == len(activas) + 1:
        print("Operación cancelada.")
        return
    ins_seleccionada = activas[opcion - 1]
    resultado = gestor_inscripciones.dar_baja_inscripcion(
        socio.numero_socio, ins_seleccionada.id_actividad, ins_seleccionada.turno
    )
    print(resultado)

def ver_actividades_socio():
    identificador = input_str("Ingrese DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    inscripciones = gestor_inscripciones.listar_actividades_de_socio(socio.numero_socio)
    if not inscripciones:
        print("El socio no tiene inscripciones.")
        return
    print("\n--- Inscripciones del socio ---")
    hoy = date.today()
    for ins in inscripciones:
        act = gestor_actividades.obtener_actividad(ins.id_actividad)
        nombre = act.nombre if act else "Desconocida"
        estado = "Activa" if ins.activa and ins.fecha_fin >= hoy else "Inactiva/Vencida"
        print(
            f"Actividad: {nombre} | Turno: {ins.turno.capitalize()} | "
            f"Inicio: {ins.fecha_inicio.strftime('%Y-%m-%d')} | "
            f"Fin: {ins.fecha_fin.strftime('%Y-%m-%d')} | Estado: {estado}"
        )

def ver_socios_actividad():
    # Obtener todas las actividades activas
    actividades = gestor_actividades.listar_activas()
    if not actividades:
        print("No hay actividades activas.")
        return
    print("\n--- Actividades disponibles ---")
    for idx, act in enumerate(actividades, 1):
        print(f"{idx}. {act.nombre}")
    print(f"{len(actividades)+1}. Cancelar")
    opcion = input_int("Seleccione una actividad: ", min=1, max=len(actividades)+1)
    if opcion == len(actividades)+1:
        print("Operación cancelada.")
        return
    act = actividades[opcion-1]
    print(f"\n--- {act.nombre} ---")
    print("\nSeleccione el turno:")
    for idx, turno in enumerate(act.turnos, 1):
        print(f"{idx}. {turno.capitalize()}")
    print(f"{len(act.turnos)+1}. Cancelar")
    opcion_turno = input_int("Seleccione un turno: ", min=1, max=len(act.turnos) + 1)
    if opcion_turno == len(act.turnos) + 1:
        print("Operación cancelada.")
        return
    turno = act.turnos[opcion_turno - 1]
    socios_ids = gestor_inscripciones.listar_socios_en_actividad_turno(act.id, turno)
    if not socios_ids:
        print("No hay socios inscritos activamente en este turno.")
        return
    print(f"\n--- Socios inscritos en {act.nombre} - Turno {turno.capitalize()} ---")
    for num in socios_ids:
        socio = gestor_socios.buscar_por_numero(num)
        if socio and socio.activo:
            print(f"Socio num {num} - {socio.nombre_completo}")