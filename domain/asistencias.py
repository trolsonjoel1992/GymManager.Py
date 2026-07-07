from dataclasses import dataclass
from datetime import date


@dataclass
class Asistencia:
    id: int
    numero_socio: int
    id_actividad: int
    turno: str  # "mañana", "tarde", "noche" (siempre presente)
    fecha: date
    presente: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero_socio": self.numero_socio,
            "id_actividad": self.id_actividad,
            "turno": self.turno,
            "fecha": self.fecha.isoformat(),
            "presente": self.presente,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Asistencia":
        return cls(
            id=data["id"],
            numero_socio=data["numero_socio"],
            id_actividad=data["id_actividad"],
            turno=data["turno"],
            fecha=date.fromisoformat(data["fecha"]),
            presente=data.get("presente", True),
        )