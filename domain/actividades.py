from dataclasses import dataclass

@dataclass
class Actividad:
    id: int
    nombre: str
    descripcion: str
    horario: str
    cupo: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "horario": self.horario,
            "cupo": self.cupo
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Actividad':
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            horario=data["horario"],
            cupo=data["cupo"]
        )