from typing import Dict, List, Optional
from domain.actividades import Actividad
from persistence import repositorio_actividades as repo_act
from persistence import repositorio_inscripciones as repo_insc

ID_MUSCULACION = 1

def listar_actividades_disponibles() -> List[Dict]:
    todas = repo_act.listar_activas()
    resultado = []
    for act in todas:
        turnos_con_cupo = []
        for turno in act.turnos:
            inscritos = repo_insc.contar_inscritos_activos(act.id, turno)
            cupo = act.cupo_por_turno(turno)
            if cupo > 0 and inscritos < cupo:
                turnos_con_cupo.append(turno)
        if turnos_con_cupo:
            resultado.append({
                "id": act.id,
                "nombre": act.nombre,
                "descripcion": act.descripcion,
                "turnos_disponibles": turnos_con_cupo,
            })
    return resultado

def obtener_actividad(id_actividad: int) -> Optional[Actividad]:
    return repo_act.obtener_actividad(id_actividad)

def obtener_actividad_por_nombre(nombre: str) -> Optional[Actividad]:
    return repo_act.obtener_actividad_nombre(nombre)

def obtener_turnos_con_cupo(id_actividad: int) -> List[str]:
    act = repo_act.obtener_actividad(id_actividad)
    if not act or not act.activa:
        return []
    disponibles = []
    for turno in act.turnos:
        inscritos = repo_insc.contar_inscritos_activos(id_actividad, turno)
        if inscritos < act.cupo_por_turno(turno):
            disponibles.append(turno)
    return disponibles

def es_musculacion(id_actividad: int) -> bool:
    return id_actividad == ID_MUSCULACION