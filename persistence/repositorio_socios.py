import json
import os
from typing import List, Optional
from domain.socios import Socio

DATA_DIR = "files"
SOCIOS_FILE = os.path.join(DATA_DIR, "socios.json")

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def cargar_socios() -> List[Socio]:
    _asegurar_directorio()
    if not os.path.exists(SOCIOS_FILE):
        return []
    with open(SOCIOS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Socio.from_dict(item) for item in data]

def guardar_socios(socios: List[Socio]):
    _asegurar_directorio()
    with open(SOCIOS_FILE, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in socios], f, indent=4, ensure_ascii=False)

def actualizar_socio(socio_actualizado: Socio) -> bool:
    """
    Busca un socio por número y lo reemplaza en el archivo.
    Retorna True si se encontró y actualizó, False en caso contrario.
    """
    socios = cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio_actualizado.numero_socio:
            socios[i] = socio_actualizado
            guardar_socios(socios)
            return True
    return False

def existe_dni(dni: str, socios: List[Socio]) -> bool:
    return any(s.dni == dni for s in socios)

def buscar_por_dni(dni: str) -> Optional[Socio]:
    socios = cargar_socios()
    for s in socios:
        if s.dni == dni:
            return s
    return None

def buscar_por_numero(numero: int) -> Optional[Socio]:
    socios = cargar_socios()
    for s in socios:
        if s.numero_socio == numero:
            return s
    return None