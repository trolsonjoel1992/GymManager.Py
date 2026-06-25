import json
import os
from typing import List
from domain.pagos import Pago

DATA_DIR = "files"
PAGOS_FILE = os.path.join(DATA_DIR, "pagos.json")

def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)

def cargar_pagos() -> List[Pago]:
    _asegurar_directorio()
    if not os.path.exists(PAGOS_FILE):
        return []
    with open(PAGOS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Pago.from_dict(item) for item in data]

def guardar_pagos(pagos: List[Pago]):
    _asegurar_directorio()
    with open(PAGOS_FILE, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in pagos], f, indent=4, ensure_ascii=False)

def agregar_pago(pago: Pago):
    pagos = cargar_pagos()
    pagos.append(pago)
    guardar_pagos(pagos)

def obtener_pagos_por_socio(numero_socio: int) -> List[Pago]:
    pagos = cargar_pagos()
    return [p for p in pagos if p.numero_socio == numero_socio]

def obtener_ultimo_pago(numero_socio: int) -> Pago:
    pagos = obtener_pagos_por_socio(numero_socio)
    if not pagos:
        return None
    return max(pagos, key=lambda p: p.fecha_pago)