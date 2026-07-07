from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Inscripcion:
    id: int
    numero_socio: int
    id_actividad: int
    turno: str  # "maÃ±ana", "tarde", "noche"
    fecha_inicio: date
    fecha_fin: date
    activa: bool = True
    fecha_baja: Optional[date] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero_socio": self.numero_socio,
            "id_actividad": self.id_actividad,
            "turno": self.turno,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "activa": self.activa,
            "fecha_baja": self.fecha_baja.isoformat() if self.fecha_baja else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Inscripcion":
        return cls(
            id=data["id"],
            numero_socio=data["numero_socio"],
            id_actividad=data["id_actividad"],
            turno=data["turno"],
            fecha_inicio=date.fromisoformat(data["fecha_inicio"]),
            fecha_fin=date.fromisoformat(data["fecha_fin"]),
            activa=data.get("activa", True),
            fecha_baja=date.fromisoformat(data["fecha_baja"]) if data.get("fecha_baja") else None,
        )