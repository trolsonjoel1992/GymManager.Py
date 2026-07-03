from datetime import date
from typing import List
from domain.inscripciones import Inscripcion
from persistence import repositorio_inscripciones as repo_insc
from services import gestor_actividades, gestor_socios

ID_MUSCULACION = gestor_actividades.ID_MUSCULACION

def inscribir_socio(numero_socio: int, id_actividad: int, turno: str) -> str:
    socio = gestor_socios.buscar_por_identificador(str(numero_socio))
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo. No puede inscribirse."
    actividad = gestor_actividades.obtener_actividad(id_actividad)
    if not actividad or not actividad.activa:
        return "Actividad no disponible."
    if turno not in actividad.turnos:
        return "Turno no válido para esta actividad."
    inscritos = repo_insc.contar_inscritos_activos(id_actividad, turno)
    cupo = actividad.cupo_por_turno(turno)
    if inscritos >= cupo:
        return "No hay cupo disponible en este turno."
    existente = repo_insc.obtener_activa(numero_socio, id_actividad, turno)
    if existente:
        return "El socio ya está inscrito en esta actividad y turno."
    if id_actividad != ID_MUSCULACION:
        inscripciones_socio = repo_insc.obtener_por_socio(numero_socio)
        activas_socio = [
            i
            for i in inscripciones_socio
            if i.activa and i.fecha_fin >= date.today() and i.id_actividad != ID_MUSCULACION
        ]
        limite = 2 if socio.membresia == "basica" else 4
        if len(activas_socio) >= limite:
            return f"Límite de actividades adicionales alcanzado ({limite})."
    if not socio.fin_cobertura or socio.fin_cobertura < date.today():
        return "El socio no tiene cobertura vigente. Debe renovar su membresía."
    nueva = Inscripcion(
        id=0,
        numero_socio=numero_socio,
        id_actividad=id_actividad,
        turno=turno,
        fecha_inicio=date.today(),
        fecha_fin=socio.fin_cobertura,
        activa=True,
        fecha_baja=None,
    )
    repo_insc.agregar(nueva)
    return "Inscripción exitosa."

def dar_baja_inscripcion(numero_socio: int, id_actividad: int, turno: str) -> str:
    insc = repo_insc.obtener_activa(numero_socio, id_actividad, turno)
    if not insc:
        return "El socio no está inscrito activamente en esa actividad y turno."
    insc.activa = False
    insc.fecha_baja = date.today()
    repo_insc.actualizar(insc)
    return "Baja de inscripción realizada."

def listar_actividades_de_socio(numero_socio: int) -> List[Inscripcion]:
    return repo_insc.obtener_por_socio(numero_socio)

def obtener_inscripciones_activas_vigentes(numero_socio: int) -> List[Inscripcion]:
    hoy = date.today()
    inscripciones = repo_insc.obtener_por_socio(numero_socio)
    return [i for i in inscripciones if i.activa and i.fecha_fin >= hoy]

def listar_socios_en_actividad_turno(id_actividad: int, turno: str) -> List[int]:
    inscritos = repo_insc.obtener_por_actividad(id_actividad)
    hoy = date.today()
    return [
        i.numero_socio for i in inscritos if i.activa and i.turno == turno and i.fecha_fin >= hoy
    ]

def extender_inscripciones(numero_socio: int, nueva_fecha_fin: date) -> None:
    inscripciones = repo_insc.obtener_por_socio(numero_socio)
    for i in inscripciones:
        if i.activa and i.fecha_fin < nueva_fecha_fin:
            i.fecha_fin = nueva_fecha_fin
            repo_insc.actualizar(i)

def inscribir_automatico_musculacion(
    numero_socio: int, fecha_inicio: date, fecha_fin: date
) -> None:
    existente = repo_insc.obtener_activa(numero_socio, ID_MUSCULACION, "mañana")
    if existente:
        return  
    nueva = Inscripcion(
        id=0,
        numero_socio=numero_socio,
        id_actividad=ID_MUSCULACION,
        turno="mañana",  
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activa=True,
        fecha_baja=None,
    )
    repo_insc.agregar(nueva)

def dar_baja_todas_inscripciones(numero_socio: int) -> None:
    inscripciones = repo_insc.obtener_por_socio(numero_socio)
    for i in inscripciones:
        if i.activa:
            i.activa = False
            i.fecha_baja = date.today()
            repo_insc.actualizar(i)
