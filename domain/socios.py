from dataclasses import dataclass, field
from datetime import date
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
    actividades: list = field(default_factory=list)
    fecha_inscripcion: date = field(default_factory=date.today)
    fecha_ultimo_pago: Optional[date] = field(default=None)
    activo: bool = True
    motivo_baja: Optional[Literal["mora", "manual"]] = field(default=None)
    fecha_cambio_membresia: Optional[date] = field(default=None)  # Nuevo campo

    def to_dict(self) -> dict:
        return {
            "numero_socio": self.numero_socio,
            "dni": self.dni,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "email": self.email,
            "membresia": self.membresia,
            "actividades": self.actividades,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat(),
            "fecha_ultimo_pago": self.fecha_ultimo_pago.isoformat() if self.fecha_ultimo_pago else None,
            "activo": self.activo,
            "motivo_baja": self.motivo_baja,
            "fecha_cambio_membresia": self.fecha_cambio_membresia.isoformat() if self.fecha_cambio_membresia else None
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
            actividades=data.get("actividades", []),
            fecha_inscripcion=date.fromisoformat(data["fecha_inscripcion"]),
            fecha_ultimo_pago=date.fromisoformat(data["fecha_ultimo_pago"]) if data.get("fecha_ultimo_pago") else None,
            activo=data["activo"],
            motivo_baja=data.get("motivo_baja"),
            fecha_cambio_membresia=date.fromisoformat(data["fecha_cambio_membresia"]) if data.get("fecha_cambio_membresia") else None
        )