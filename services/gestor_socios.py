from typing import List, Optional
from domain.socio import Socio
from persistence import repositorio

def alta_socio(dni: str, nombre: str, telefono: str, direccion: str, email: str) -> Optional[Socio]:
    """
    Da de alta un nuevo socio.
    Precondición: los datos ya han sido validados en formato por la capa de presentación.
    Retorna el socio creado o None si ya existe un DNI duplicado.
    """
    socios = repositorio.cargar_socios()
    if repositorio.existe_dni(dni, socios):
        print(f"Ya existe un socio con DNI {dni}.")
        return None
    
    nuevo_id = max([s.id for s in socios], default=0) + 1
    nuevo_socio = Socio(
        id=nuevo_id,
        dni=dni,
        nombre_completo=nombre,
        telefono=telefono,
        direccion=direccion,
        email=email
    )
    socios.append(nuevo_socio)
    repositorio.guardar_socios(socios)
    print(f"Socio {nombre} (ID {nuevo_id}) registrado correctamente.")
    return nuevo_socio

def listar_socios(mostrar_inactivos: bool = False) -> List[Socio]:
    socios = repositorio.cargar_socios()
    if mostrar_inactivos:
        return socios
    return [s for s in socios if s.activo]

def buscar_por_dni(dni: str) -> Optional[Socio]:
    socios = repositorio.cargar_socios()
    for s in socios:
        if s.dni == dni:
            return s
    return None

def buscar_por_id(id_socio: int) -> Optional[Socio]:
    socios = repositorio.cargar_socios()
    for s in socios:
        if s.id == id_socio:
            return s
    return None

def editar_socio(dni: str, nuevos_datos: dict) -> bool:
    """
    Edita un socio existente.
    nuevos_datos puede contener: nombre_completo, telefono, direccion, email.
    (No se permite cambiar DNI, ID, fecha_inscripcion ni estado activo).
    """
    socios = repositorio.cargar_socios()
    for i, s in enumerate(socios):
        if s.dni == dni:
            # No validamos formato porque asumimos que la presentación ya lo hizo
            if "nombre_completo" in nuevos_datos:
                s.nombre_completo = nuevos_datos["nombre_completo"]
            if "telefono" in nuevos_datos:
                s.telefono = nuevos_datos["telefono"]
            if "direccion" in nuevos_datos:
                s.direccion = nuevos_datos["direccion"]
            if "email" in nuevos_datos:
                s.email = nuevos_datos["email"]
            repositorio.guardar_socios(socios)
            print("Socio actualizado correctamente.")
            return True
    print(f"No se encontró socio con DNI {dni}.")
    return False

def eliminar_socio_logico(dni: str) -> bool:
    socios = repositorio.cargar_socios()
    for s in socios:
        if s.dni == dni:
            if not s.activo:
                print("El socio ya estaba inactivo.")
                return False
            s.activo = False
            repositorio.guardar_socios(socios)
            print(f"Socio {s.nombre_completo} (DNI {dni}) marcado como inactivo.")
            return True
    print(f"No se encontró socio con DNI {dni}.")
    return False