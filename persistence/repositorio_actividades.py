import json
import os
from typing import List, Optional
from domain.actividades import Actividad

ACTIVIDADES_FILE = "files/actividades.json"
DATA_DIR = "files"

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def cargar_actividades() -> List[Actividad]:
    _asegurar_directorio()
    if not os.path.exists(ACTIVIDADES_FILE):
        return []
    with open(ACTIVIDADES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Actividad(**item) for item in data]

def obtener_actividad(id_actividad: int) -> Optional[Actividad]:
    for act in cargar_actividades():
        if act.id == id_actividad:
            return act
    return None

def obtener_actividad_nombre(nombre: str) -> Optional[Actividad]:
    for act in cargar_actividades():
        if act.nombre.lower() == nombre.lower():
            return act
    return None

def listar_activas() -> List[Actividad]:
    return [a for a in cargar_actividades() if a.activa]