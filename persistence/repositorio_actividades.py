import json
import os
from typing import List, Optional
from domain.actividades import Actividad

DATA_DIR = "files"
ACTIVIDADES_FILE = os.path.join(DATA_DIR, "actividades.json")

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def cargar_actividades() -> List[Actividad]:
    _asegurar_directorio()
    if not os.path.exists(ACTIVIDADES_FILE):
        return []
    with open(ACTIVIDADES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Actividad.from_dict(item) for item in data]

def guardar_actividades(actividades: List[Actividad]):
    _asegurar_directorio()
    with open(ACTIVIDADES_FILE, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in actividades], f, indent=4, ensure_ascii=False)

def obtener_todos(self) -> list[Actividad]:
    return [Actividad.from_dict(item) for item in self._load()]

def buscar_por_nombre(nombre: str) -> Optional[Actividad]:
    nombre_lower = nombre.lower()
    actividades = cargar_actividades()
    for s in actividades:
        if s.nombre.lower() == nombre_lower:
            return s
    return None

def listar_actividades() -> List[Actividad]:
    return cargar_actividades()