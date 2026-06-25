from persistence import repositorio_actividades
from domain.actividades import Actividad
from typing import Optional


def listar_actividades():
    return repositorio_actividades.listar_actividades()

def obtener_actividad():
    print("Funcionalidad en desarrollo")

def buscar_por_nombre(nombre: str) -> Optional[Actividad]:
    return repositorio_actividades.buscar_por_nombre(nombre)
    