from datetime import date, datetime, timedelta
from typing import List, Tuple, Optional
from domain.asistencias import Asistencia
from persistence import repositorio_asistencias as repo_asist
from persistence import repositorio_inscripciones as repo_insc
from services import gestor_actividades, gestor_inscripciones, gestor_socios

LIMITE_FALTAS_MES = 12
LIMITE_FALTAS_CONSECUTIVAS = 7
ID_MUSCULACION = 1
ACTIVIDADES_EXENTAS_DE_BAJA = [ID_MUSCULACION]   # Actividades que no se dan de baja por faltas

def obtener_turno_actual() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "mañana"
    elif hora < 18:
        return "tarde"
    else:
        return "noche"

def _es_domingo(fecha: date) -> bool:
    return fecha.weekday() == 6

def _clasificar_dias(asistencias: List[Asistencia]) -> Tuple[set, set]:
    """
    Retorna (dias_con_presente, dias_con_falta)
    - Un día se considera con falta si NO hay ningún registro presente en esa fecha.
    - Si hay al menos un presente, no se considera falta (aunque tenga ausencias).
    """
    presentes = set()
    ausentes = set()
    for a in asistencias:
        if a.presente:
            presentes.add(a.fecha)
        else:
            ausentes.add(a.fecha)
    dias_falta = ausentes - presentes
    return presentes, dias_falta

def marcar_asistencia(
    numero_socio: int,
    id_actividad: int,
    turno: str,
    presente: bool = True,
    fecha: Optional[date] = None
) -> str:
    if fecha is None:
        fecha = date.today()
    if _es_domingo(fecha):
        return "No se puede marcar asistencia en domingo."
    socio = gestor_socios.buscar_por_numero(numero_socio)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo."
    actividad = gestor_actividades.obtener_actividad(id_actividad)
    if not actividad or not actividad.activa:
        return "Actividad no disponible."
    if id_actividad != ID_MUSCULACION and turno not in actividad.turnos:
        return f"Turno '{turno}' no válido para esta actividad."
    # Verificar inscripción activa
    if id_actividad == ID_MUSCULACION:
        inscripciones = repo_insc.obtener_por_socio(numero_socio)
        inscripcion_valida = None
        for ins in inscripciones:
            if (
                ins.id_actividad == id_actividad
                and ins.activa
                and ins.fecha_inicio <= fecha <= ins.fecha_fin
            ):
                inscripcion_valida = ins
                break
        if not inscripcion_valida:
            return "El socio no tiene inscripción activa en Musculación."
        turno_real = turno
    else:
        inscripcion_valida = repo_insc.obtener_activa(numero_socio, id_actividad, turno)
        if not inscripcion_valida:
            return "El socio no tiene inscripción activa en esta actividad y turno."
        turno_real = turno

    existente = repo_asist.obtener_por_socio_actividad_turno_fecha(
        numero_socio, id_actividad, turno_real, fecha
    )
    if existente:
        if existente.presente == presente:
            return "La asistencia ya estaba registrada con el mismo estado."
        existente.presente = presente
        repo_asist.actualizar(existente)
        return "Asistencia actualizada."
    else:
        asist = Asistencia(
            id=0,
            numero_socio=numero_socio,
            id_actividad=id_actividad,
            turno=turno_real,
            fecha=fecha,
            presente=presente
        )
        repo_asist.agregar(asist)
        return "Asistencia registrada."

def corregir_asistencia(id_asistencia: int, nuevo_presente: bool) -> str:
    asistencia = repo_asist.obtener_por_id(id_asistencia)
    if not asistencia:
        return "Asistencia no encontrada."
    if asistencia.fecha != date.today():
        return "Solo se pueden corregir asistencias del día actual."
    if asistencia.presente == nuevo_presente:
        return "La asistencia ya tiene ese estado."
    asistencia.presente = nuevo_presente
    repo_asist.actualizar(asistencia)
    return f"Asistencia corregida a {'Presente' if nuevo_presente else 'Ausente'}."

def obtener_faltas_socio(
    numero_socio: int,
    id_actividad: int,
    turno: Optional[str] = None
) -> Tuple[int, int]:
    """
    Retorna (faltas_mes, faltas_consecutivas) para un socio en una actividad.
    Para musculación (id=1) se ignoran los turnos y se agrupa por día.
    """
    if id_actividad != ID_MUSCULACION and turno is None:
        raise ValueError("Para actividades no musculación se requiere el turno.")
    todas = repo_asist.obtener_por_socio_actividad(numero_socio, id_actividad)
    if id_actividad != ID_MUSCULACION:
        todas = [a for a in todas if a.turno == turno]
    if not todas:
        return (0, 0)
    dias_presente, dias_falta = _clasificar_dias(todas)
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    # Faltas en el mes actual (días)
    faltas_mes = sum(1 for d in dias_falta if inicio_mes <= d <= hoy)
    # Faltas consecutivas desde hoy hacia atrás
    faltas_consec = 0
    fecha_actual = hoy
    while True:
        if fecha_actual in dias_falta:
            faltas_consec += 1
            fecha_actual -= timedelta(days=1)
        elif fecha_actual in dias_presente:
            # Hubo presencia, la racha se rompe
            break
    return (faltas_mes, faltas_consec)

def obtener_asistencias_socio_dia(numero_socio: int, fecha: date) -> List[Asistencia]:
    todas = repo_asist.obtener_por_socio(numero_socio)
    return [a for a in todas if a.fecha == fecha]

def procesar_bajas_por_faltas() -> int:
    """
    Recorre todas las inscripciones activas y vigentes,
    evalúa si el socio ha alcanzado el límite de faltas,
    y en caso afirmativo da de baja la inscripción.
    EXCLUYE la actividad Musculación (ID=1) y cualquier otra
    que se añada a ACTIVIDADES_EXENTAS_DE_BAJA.
    Retorna la cantidad de bajas realizadas.
    """
    inscripciones = repo_insc.obtener_todas_activas_vigentes()
    bajas = 0
    for ins in inscripciones:
        if ins.id_actividad in ACTIVIDADES_EXENTAS_DE_BAJA:
            continue
        faltas_mes, faltas_consec = obtener_faltas_socio(
            ins.numero_socio, ins.id_actividad, ins.turno
        )
        if faltas_mes >= LIMITE_FALTAS_MES or faltas_consec >= LIMITE_FALTAS_CONSECUTIVAS:
            gestor_inscripciones.dar_baja_inscripcion(
                ins.numero_socio, ins.id_actividad, ins.turno
            )
            bajas += 1
    return bajas