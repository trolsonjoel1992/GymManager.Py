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
    fecha_inscripcion: date = field(default_factory=date.today)
    fin_cobertura: Optional[date] = field(default=None)
    activo: bool = True
    motivo_baja: Optional[Literal["mora", "manual"]] = field(default=None)
    fecha_cambio_membresia: Optional[date] = field(default=None)
    fecha_baja: Optional[date] = field(default=None)  # NUEVO CAMPO

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
            "fin_cobertura": self.fin_cobertura.isoformat() if self.fin_cobertura else None,
            "activo": self.activo,
            "motivo_baja": self.motivo_baja,
            "fecha_cambio_membresia": (
                self.fecha_cambio_membresia.isoformat() if self.fecha_cambio_membresia else None
            ),
            "fecha_baja": self.fecha_baja.isoformat() if self.fecha_baja else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Socio":
        return cls(
            numero_socio=data["numero_socio"],
            dni=data["dni"],
            nombre_completo=data["nombre_completo"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            email=data["email"],
            membresia=data["membresia"],
            fecha_inscripcion=date.fromisoformat(data["fecha_inscripcion"]),
            fin_cobertura=(
                date.fromisoformat(data["fin_cobertura"]) if data.get("fin_cobertura") else None
            ),
            activo=data["activo"],
            motivo_baja=data.get("motivo_baja"),
            fecha_cambio_membresia=(
                date.fromisoformat(data["fecha_cambio_membresia"])
                if data.get("fecha_cambio_membresia")
                else None
            ),
            fecha_baja=date.fromisoformat(data["fecha_baja"]) if data.get("fecha_baja") else None,
        )