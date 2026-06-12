from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class Socio:
    id: int                         # Número de socio (autogenerado)
    dni: str                        # Clave única
    nombre_completo: str
    telefono: str
    direccion: str
    email: str
    fecha_inscripcion: date = field(default_factory=date.today)
    activo: bool = True             # Borrado lógico
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para JSON."""
        return {
            "id": self.id,
            "dni": self.dni,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "email": self.email,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat(),
            "activo": self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Socio':
        """Crea un objeto Socio desde un diccionario."""
        return cls(
            id=data["id"],
            dni=data["dni"],
            nombre_completo=data["nombre_completo"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            email=data["email"],
            fecha_inscripcion=date.fromisoformat(data["fecha_inscripcion"]),
            activo=data["activo"]
        )