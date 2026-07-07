from dataclasses import dataclass
from typing import List


@dataclass
class Actividad:
    id: int
    nombre: str
    descripcion: str
    cupo_manana: int
    cupo_tarde: int
    cupo_noche: int
    turnos: List[str]  # lista de turnos disponibles (ej: ["mañana", "tarde"])
    activa: bool = True

    def cupo_por_turno(self, turno: str) -> int:
        if turno == "mañana":
            return self.cupo_manana
        elif turno == "tarde":
            return self.cupo_tarde
        elif turno == "noche":
            return self.cupo_noche
        return 0