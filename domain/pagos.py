from dataclasses import dataclass
from datetime import date
from typing import Literal

@dataclass
class Pago:
    id: int
    numero_socio: int
    fecha_pago: date
    monto: float
    meses_cubiertos: int
    membresia: Literal["basica", "premium"]
    observaciones: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero_socio": self.numero_socio,
            "fecha_pago": self.fecha_pago.isoformat(),
            "monto": self.monto,
            "meses_cubiertos": self.meses_cubiertos,
            "membresia": self.membresia,
            "observaciones": self.observaciones
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Pago':
        return cls(
            id=data["id"],
            numero_socio=data["numero_socio"],
            fecha_pago=date.fromisoformat(data["fecha_pago"]),
            monto=data["monto"],
            meses_cubiertos=data["meses_cubiertos"],
            membresia=data["membresia"],
            observaciones=data.get("observaciones", "")
        )