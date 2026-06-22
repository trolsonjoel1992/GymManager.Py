from dataclasses import dataclass
from datetime import date

@dataclass
class Pago:
    id: int
    numero_socio: int           # Relación con el socio
    fecha_pago: date
    monto: float
    meses_cubiertos: int        # Número de meses que cubre este pago (1,2,3...)
    observaciones: str = ""     # Opcional

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero_socio": self.numero_socio,
            "fecha_pago": self.fecha_pago.isoformat(),
            "monto": self.monto,
            "meses_cubiertos": self.meses_cubiertos,
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
            observaciones=data.get("observaciones", "")
        )