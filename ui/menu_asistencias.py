from datetime import date
from typing import List
from services import gestor_actividades, gestor_asistencias, gestor_inscripciones, gestor_socios
from utils.inputs import input_choice, input_confirm, input_int, input_str
from domain.socios import Socio
import time

ID_MUSCULACION = 1

def mostrar_submenu():
    while True:
        print("\n--- CONTROL DE ASISTENCIA ---")
        print("1. Marcar asistencia individual (musculación)")
        print("2. Marcar asistencia masiva (por actividad y turno)")
        print("3. Historial de faltas de un socio")
        print("4. Ver faltas por actividad")
        print("5. Corregir asistencia del día actual")
        print("6. Volver al menú principal")
        opcion = input_int("Seleccione una opción: ", min=1, max=6)
        if opcion == 1:
            marcar_asistencia_individual()
        elif opcion == 2:
            marcar_asistencia_masiva()
        elif opcion == 3:
            historial_faltas_socio()
        elif opcion == 4:
            ver_faltas_por_actividad()
        elif opcion == 5:
            corregir_asistencia()
        elif opcion == 6:
            break

def marcar_asistencia_individual():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    mostrar_estado_cuota(socio)
    if not socio.activo:
        print("El socio está inactivo. No se puede registrar asistencia.")
        return
    actividad = gestor_actividades.obtener_actividad(ID_MUSCULACION)
    if not actividad or not actividad.activa:
        print("La actividad Musculación no está disponible actualmente.")
        return
    turno_actual = gestor_asistencias.obtener_turno_actual()
    # Verificar inscripción (la inscripción en musculación es única con turno "mañana")
    inscripcion = gestor_inscripciones.obtener_activa(socio.numero_socio, ID_MUSCULACION, "mañana")
    if not inscripcion or not inscripcion.activa:
        print("El socio no está inscrito en Musculación. No puede marcar asistencia.")
        return
    resultado = gestor_asistencias.marcar_asistencia(
        socio.numero_socio, ID_MUSCULACION, turno_actual, presente=True
    )
    print(resultado)

def marcar_asistencia_masiva():
    # --- Proceso batch de actualización y bajas ---
    print("\nActualizando listas de inscriptos", end="", flush=True)
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print(" ¡Listo!")
    # Ejecutar el proceso de bajas automáticas por faltas (incluye todas las actividades)
    bajas = gestor_asistencias.procesar_bajas_por_faltas()
    if bajas > 0:
        print(f"Se han dado de baja {bajas} inscripción(es) por exceso de faltas.")
    else:
        print("No se dieron de baja inscripciones.")
    # --- Obtener actividades con inscriptos (excluyendo musculación) ---
    actividades_con_inscriptos = _obtener_actividades_con_inscriptos()
    if not actividades_con_inscriptos:
        print("\nNo hay actividades con socios inscriptos actualmente.")
        return
    print("\n--- Actividades con socios inscriptos ---")
    for idx, (id_act, nombre) in enumerate(actividades_con_inscriptos, 1):
        print(f"{idx}. {nombre}")
    print(f"{len(actividades_con_inscriptos)+1}. Cancelar")
    opcion_act = input_int("Seleccione una actividad: ", min=1, max=len(actividades_con_inscriptos)+1)
    if opcion_act == len(actividades_con_inscriptos)+1:
        print("Operación cancelada.")
        return
    id_actividad_seleccionada = actividades_con_inscriptos[opcion_act-1][0]
    actividad = gestor_actividades.obtener_actividad(id_actividad_seleccionada)
    if not actividad:
        print("Actividad no encontrada.")
        return
    # --- Obtener turnos con inscriptos para esa actividad ---
    turnos_con_inscriptos = _obtener_turnos_con_inscriptos(actividad.id)
    if not turnos_con_inscriptos:
        print("No hay turnos con inscriptos para esta actividad.")
        return
    print(f"\n--- Turnos con inscriptos en {actividad.nombre} ---")
    for idx, turno in enumerate(turnos_con_inscriptos, 1):
        print(f"{idx}. {turno.capitalize()}")
    print(f"{len(turnos_con_inscriptos)+1}. Cancelar")
    opcion_turno = input_int("Seleccione un turno: ", min=1, max=len(turnos_con_inscriptos)+1)
    if opcion_turno == len(turnos_con_inscriptos)+1:
        print("Operación cancelada.")
        return
    turno_elegido = turnos_con_inscriptos[opcion_turno-1]
    # --- Obtener socios inscriptos en ese turno ---
    socios_ids = gestor_inscripciones.listar_socios_en_actividad_turno(actividad.id, turno_elegido)
    if not socios_ids:
        print("No hay socios inscritos en este turno.")
        return
    print(f"\n--- Marcación de asistencia para {actividad.nombre} - Turno {turno_elegido.capitalize()} ---")
    print("Por cada socio, ingrese P (presente) o A (ausente).")
    print("(Si ya tiene asistencia registrada hoy, se omitirá)\n")
    contador = 0
    for num in socios_ids:
        socio = gestor_socios.buscar_por_numero(num)
        if not socio:
            continue
        mostrar_estado_cuota(socio, compacto=True)
        respuesta = input_choice(
            f"{socio.nombre_completo} (N°{socio.numero_socio}) - P/A: ",
            ["P", "A", "p", "a"]
        ).upper()
        presente = (respuesta == "P")
        resultado = gestor_asistencias.marcar_asistencia(
            socio.numero_socio,
            actividad.id,
            turno_elegido,
            presente=presente
        )
        if "registrada" in resultado or "actualizada" in resultado:
            contador += 1
        print(f"  -> {resultado}")
    print(f"\nProceso finalizado. {contador} asistencias procesadas.")

def historial_faltas_socio():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    inscripciones = gestor_inscripciones.obtener_inscripciones_activas_vigentes(socio.numero_socio)
    if not inscripciones:
        print("El socio no tiene inscripciones activas.")
        return
    print("\n--- Actividades en las que está inscrito ---")
    opciones = []
    for idx, ins in enumerate(inscripciones, 1):
        act = gestor_actividades.obtener_actividad(ins.id_actividad)
        if act:
            nombre = act.nombre
            if ins.id_actividad != ID_MUSCULACION:
                nombre += f" ({ins.turno.capitalize()})"
            print(f"{idx}. {nombre}")
            opciones.append((ins.id_actividad, ins.turno))
    print(f"{len(opciones)+1}. Volver")
    opcion = input_int("Seleccione una actividad para ver sus faltas: ", min=1, max=len(opciones)+1)
    if opcion == len(opciones)+1:
        return
    id_actividad, turno = opciones[opcion-1]
    faltas_mes, faltas_consec = gestor_asistencias.obtener_faltas_socio(
        socio.numero_socio, id_actividad, turno
    )
    actividad = gestor_actividades.obtener_actividad(id_actividad)
    nombre_act = actividad.nombre if actividad else "Desconocida"
    print(f"\n--- Faltas en {nombre_act} ---")
    print(f"Faltas en el mes actual: {faltas_mes}")
    print(f"Faltas consecutivas (hasta hoy): {faltas_consec}")

def ver_faltas_por_actividad():
    # Obtener actividades activas excepto musculación
    actividades = [act for act in gestor_actividades.listar_activas() if act.id != ID_MUSCULACION]
    if not actividades:
        print("No hay actividades activas para consultar faltas.")
        return
    print("\n--- Actividades disponibles ---")
    for idx, act in enumerate(actividades, 1):
        print(f"{idx}. {act.nombre}")
    print(f"{len(actividades)+1}. Cancelar")
    opcion = input_int("Seleccione una actividad: ", min=1, max=len(actividades)+1)
    if opcion == len(actividades)+1:
        print("Operación cancelada.")
        return
    actividad = actividades[opcion-1]
    # Turnos disponibles (igual que antes)
    print("\nTurnos disponibles:")
    for idx, turno in enumerate(actividad.turnos, 1):
        print(f"{idx}. {turno.capitalize()}")
    print(f"{len(actividad.turnos)+1}. Cancelar")
    opcion_turno = input_int("Seleccione un turno: ", min=1, max=len(actividad.turnos)+1)
    if opcion_turno == len(actividad.turnos)+1:
        print("Operación cancelada.")
        return
    turno_elegido = actividad.turnos[opcion_turno-1]
    socios_ids = gestor_inscripciones.listar_socios_en_actividad_turno(actividad.id, turno_elegido)
    if not socios_ids:
        print("No hay socios inscritos en este turno.")
        return
    print(f"\n--- Faltas en {actividad.nombre} - Turno {turno_elegido.capitalize()} ---")
    print("Socio | Faltas en el mes | Faltas consecutivas")
    for num in socios_ids:
        socio = gestor_socios.buscar_por_numero(num)
        if not socio:
            continue
        faltas_mes, faltas_cons = gestor_asistencias.obtener_faltas_socio(
            socio.numero_socio, actividad.id, turno_elegido
        )
        print(f"{socio.nombre_completo} (N°{socio.numero_socio}) | {faltas_mes} | {faltas_cons}")

def corregir_asistencia():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    hoy = date.today()
    asistencias_hoy = gestor_asistencias.obtener_asistencias_socio_dia(socio.numero_socio, hoy)
    if not asistencias_hoy:
        print("No hay asistencias registradas hoy para este socio.")
        return
    print("\n--- Asistencias del día de hoy ---")
    for idx, asist in enumerate(asistencias_hoy, 1):
        act = gestor_actividades.obtener_actividad(asist.id_actividad)
        nombre_act = act.nombre if act else "Desconocida"
        estado = "Presente" if asist.presente else "Ausente"
        print(f"{idx}. {nombre_act} - Turno: {asist.turno} - {estado}")
    print(f"{len(asistencias_hoy)+1}. Cancelar")
    opcion = input_int("Seleccione la asistencia a corregir: ", min=1, max=len(asistencias_hoy)+1)
    if opcion == len(asistencias_hoy)+1:
        print("Operación cancelada.")
        return
    asist_seleccionada = asistencias_hoy[opcion-1]
    nuevo_estado = not asist_seleccionada.presente
    nuevo_texto = "Presente" if nuevo_estado else "Ausente"
    if not input_confirm(f"¿Cambiar a {nuevo_texto}? (s/n): "):
        print("Corrección cancelada.")
        return
    resultado = gestor_asistencias.corregir_asistencia(
        asist_seleccionada.id, nuevo_estado
    )
    print(resultado)

def mostrar_estado_cuota(socio: Socio, compacto: bool = False):
    estado = gestor_socios.obtener_estado(socio)
    if estado == "activo":
        if compacto:
            print("  (Cuota al día)")
        else:
            print("Socio al día con su cuota.")
    elif estado == "debe_cuota":
        dias = gestor_socios.dias_desde_vencimiento(socio)
        if compacto:
            print(f"Mora ({dias} días de atraso)")
        else:
            print(f"El socio está en período de gracia. Adeuda {dias} días.")
    elif estado == "inactivo_por_deuda":
        if compacto:
            print("Inactivo por deuda")
        else:
            print("El socio está inactivo por falta de pago.")
    elif estado == "inactivo":
        if compacto:
            print("Inactivo (baja manual)")
        else:
            print("El socio está inactivo.")
    else:
        if compacto:
            print("Estado desconocido")
        else:
            print("Estado desconocido.")

def _obtener_actividades_con_inscriptos() -> List[tuple]:
    """
    Retorna una lista de tuplas (id_actividad, nombre) para aquellas actividades
    activas que tienen al menos un socio inscrito en algún turno,
    EXCLUYENDO MUSCULACIÓN (ID = 1).
    """
    actividades = gestor_actividades.listar_activas()
    resultado = []
    for act in actividades:
        # Saltar musculación
        if act.id == ID_MUSCULACION:
            continue
        # Verificar si hay al menos un inscripto en alguno de sus turnos
        tiene_inscriptos = False
        for turno in act.turnos:
            socios = gestor_inscripciones.listar_socios_en_actividad_turno(act.id, turno)
            if socios:
                tiene_inscriptos = True
                break
        if tiene_inscriptos:
            resultado.append((act.id, act.nombre))
    return resultado

def _obtener_turnos_con_inscriptos(id_actividad: int) -> List[str]:
    """
    Retorna una lista de turnos que tienen al menos un socio inscrito
    para la actividad dada.
    """
    actividad = gestor_actividades.obtener_actividad(id_actividad)
    if not actividad:
        return []
    turnos_con_inscriptos = []
    for turno in actividad.turnos:
        socios = gestor_inscripciones.listar_socios_en_actividad_turno(id_actividad, turno)
        if socios:
            turnos_con_inscriptos.append(turno)
    return turnos_con_inscriptos