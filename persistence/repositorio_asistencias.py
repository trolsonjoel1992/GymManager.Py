import json
import os
from datetime import date, timedelta
from typing import List, Optional
from domain.asistencias import Asistencia

ASISTENCIAS_FILE = "files/asistencias.json"
DATA_DIR = "files"

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def _cargar() -> List[Asistencia]:
    _asegurar_directorio()
    if not os.path.exists(ASISTENCIAS_FILE):
        return []
    with open(ASISTENCIAS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Asistencia.from_dict(item) for item in data]

def _guardar(asistencias: List[Asistencia]) -> None:
    _asegurar_directorio()
    with open(ASISTENCIAS_FILE, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in asistencias], f, indent=4, default=str)


def obtener_todas() -> List[Asistencia]:
    return _cargar()

def obtener_por_id(id_asistencia: int) -> Optional[Asistencia]:
    for a in _cargar():
        if a.id == id_asistencia:
            return a
    return None

def obtener_por_socio(numero_socio: int) -> List[Asistencia]:
    return [a for a in _cargar() if a.numero_socio == numero_socio]

def obtener_por_actividad(id_actividad: int) -> List[Asistencia]:
    return [a for a in _cargar() if a.id_actividad == id_actividad]

def obtener_por_socio_actividad(numero_socio: int, id_actividad: int) -> List[Asistencia]:
    return [
        a
        for a in _cargar()
        if a.numero_socio == numero_socio and a.id_actividad == id_actividad
    ]

def obtener_por_socio_actividad_turno_fecha(
    numero_socio: int,
    id_actividad: int,
    turno: str,
    fecha: date
) -> Optional[Asistencia]:
    for a in _cargar():
        if (
            a.numero_socio == numero_socio
            and a.id_actividad == id_actividad
            and a.turno == turno
            and a.fecha == fecha
        ):
            return a
    return None

def agregar(asistencia: Asistencia) -> None:
    asistencias = _cargar()
    max_id = max([a.id for a in asistencias], default=0) + 1
    asistencia.id = max_id
    asistencias.append(asistencia)
    _guardar(asistencias)

def actualizar(asistencia: Asistencia) -> None:
    asistencias = _cargar()
    for idx, a in enumerate(asistencias):
        if a.id == asistencia.id:
            asistencias[idx] = asistencia
            break
    _guardar(asistencias)

def contar_faltas_mes(
    numero_socio: int,
    id_actividad: int,
    turno: Optional[str] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None
) -> int:
    hoy = date.today()
    if mes is None:
        mes = hoy.month
    if anio is None:
        anio = hoy.year
    asistencias = obtener_por_socio_actividad(numero_socio, id_actividad)
    if turno is not None:
        asistencias = [a for a in asistencias if a.turno == turno]
    return sum(
        1
        for a in asistencias
        if not a.presente
        and a.fecha.year == anio
        and a.fecha.month == mes
    )

def contar_faltas_consecutivas(
    numero_socio: int,
    id_actividad: int,
    turno: Optional[str] = None,
    hasta: Optional[date] = None
) -> int:
    if hasta is None:
        hasta = date.today()
    asistencias = obtener_por_socio_actividad(numero_socio, id_actividad)
    if turno is not None:
        asistencias = [a for a in asistencias if a.turno == turno]
    asistencias.sort(key=lambda a: a.fecha, reverse=True)
    registro = {}
    for a in asistencias:
        if a.fecha not in registro:
            registro[a.fecha] = a.presente
        else:
            if a.presente:
                registro[a.fecha] = True
    faltas = 0
    fecha_actual = hasta
    while True:
        if fecha_actual not in registro:
            break
        if registro[fecha_actual]:
            break
        faltas += 1
        fecha_actual = fecha_actual - timedelta(days=1)
        if (hasta - fecha_actual).days > 31:
            break
    return faltas