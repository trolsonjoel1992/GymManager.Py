from dataclasses import dataclass, field
from datetime import date
from typing import Literal

@dataclass
class Socio:
    numero_socio: int                     # Autogenerado, único
    dni: str                              # Clave única
    nombre_completo: str
    telefono: str
    direccion: str
    email: str
    membresia: Literal["basica", "premium"]   # Nueva
    fecha_inscripcion: date = field(default_factory=date.today)
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
            activo=data["activo"]
        )