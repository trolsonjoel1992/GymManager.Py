import json
import os
from datetime import date
from typing import List, Optional
from domain.inscripciones import Inscripcion

INSCRIPCIONES_FILE = "files/inscripciones.json"
DATA_DIR = "files"

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def _cargar() -> List[Inscripcion]:
    _asegurar_directorio()
    if not os.path.exists(INSCRIPCIONES_FILE):
        return []
    with open(INSCRIPCIONES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Inscripcion.from_dict(item) for item in data]

def _guardar(inscripciones: List[Inscripcion]) -> None:
    _asegurar_directorio()
    with open(INSCRIPCIONES_FILE, "w", encoding="utf-8") as f:
        json.dump([i.to_dict() for i in inscripciones], f, indent=4, ensure_ascii=False)

def obtener_todas() -> List[Inscripcion]:
    return _cargar()

def obtener_por_socio(numero_socio: int) -> List[Inscripcion]:
    return [i for i in _cargar() if i.numero_socio == numero_socio]

def obtener_por_actividad(id_actividad: int) -> List[Inscripcion]:
    return [i for i in _cargar() if i.id_actividad == id_actividad]

def obtener_activa(numero_socio: int, id_actividad: int, turno: str) -> Optional[Inscripcion]:
    for i in _cargar():
        if (
            i.numero_socio == numero_socio
            and i.id_actividad == id_actividad
            and i.turno == turno
            and i.activa
        ):
            return i
    return None

def contar_inscritos_activos(id_actividad: int, turno: str) -> int:
    """Cuenta inscripciones activas para una actividad y turno específicos (fecha_fin >= hoy)."""
    hoy = date.today()
    return len(
        [
            i
            for i in _cargar()
            if i.id_actividad == id_actividad
            and i.turno == turno
            and i.activa
            and i.fecha_fin >= hoy
        ]
    )

def agregar(inscripcion: Inscripcion) -> None:
    inscripciones = _cargar()
    max_id = max([i.id for i in inscripciones], default=0) + 1
    inscripcion.id = max_id
    inscripciones.append(inscripcion)
    _guardar(inscripciones)

def actualizar(inscripcion: Inscripcion) -> None:
    inscripciones = _cargar()
    for idx, i in enumerate(inscripciones):
        if i.id == inscripcion.id:
            inscripciones[idx] = inscripcion
            break
    _guardar(inscripciones)

def eliminar_por_socio_actividad_turno(numero_socio: int, id_actividad: int, turno: str) -> None:
    inscripciones = _cargar()
    nuevas = [
        i
        for i in inscripciones
        if not (
            i.numero_socio == numero_socio and i.id_actividad == id_actividad and i.turno == turno
        )
    ]
    _guardar(nuevas)

def obtener_todas_activas_vigentes() -> List[Inscripcion]:
    """
    Retorna todas las inscripciones que están activas y cuya fecha_fin es >= hoy.
    Utilizado por el proceso batch de bajas por faltas.
    """
    hoy = date.today()
    return [i for i in _cargar() if i.activa and i.fecha_fin >= hoy]