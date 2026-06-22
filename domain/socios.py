from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Literal, Optional

@dataclass
class Socio:
    numero_socio: int
    dni: str
    nombre_completo: str
    telefono: str
    direccion: str
    email: str
    membresia: Literal["basica", "premium"]
    fecha_inscripcion: date = field(default_factory=date.today)  # alta original
    fecha_ultimo_pago: Optional[date] = field(default=None)      # última fecha de pago
    activo: bool = True

    def to_dict(self) -> dict:
        return {
            "numero_socio": self.numero_socio,
            "dni": self.dni,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "email": self.email,
            "membresia": self.membresia,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat(),
            "fecha_ultimo_pago": self.fecha_ultimo_pago.isoformat() if self.fecha_ultimo_pago else None,
            "activo": self.activo
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Socio':
        return cls(
            numero_socio=data["numero_socio"],
            dni=data["dni"],
            nombre_completo=data["nombre_completo"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            email=data["email"],
            membresia=data["membresia"],
            fecha_inscripcion=date.fromisoformat(data["fecha_inscripcion"]),
            fecha_ultimo_pago=date.fromisoformat(data["fecha_ultimo_pago"]) if data.get("fecha_ultimo_pago") else None,
            activo=data["activo"]
        )

    def fecha_vencimiento(self, meses=1) -> date:
        """Devuelve la fecha de vencimiento sumando 'meses' a fecha_ultimo_pago (o fecha_inscripcion si no hay pago)."""
        base = self.fecha_ultimo_pago if self.fecha_ultimo_pago else self.fecha_inscripcion
        return base + timedelta(days=meses * 30)