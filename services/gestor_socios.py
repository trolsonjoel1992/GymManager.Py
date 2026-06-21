from typing import List, Optional
from datetime import date, timedelta
from domain.socios import Socio
from persistence import repositorio_socios

DIAS_MES = 30

def es_moroso(socio: Socio) -> bool:
    """Devuelve True si el socio está moroso (pasó más de 30 días desde su fecha_inscripcion)"""
    if not socio.activo:
        return True
    hoy = date.today()
    return (hoy - socio.fecha_inscripcion).days > DIAS_MES

def cuotas_adeudadas(socio: Socio) -> int:
    """
    Calcula cuántas cuotas mensuales debe el socio (meses completos sin pagar).
    Se asume que el primer mes está pagado (alta).
    """
    if not socio.activo:
        return 0
    hoy = date.today()
    # Diferencia en meses
    meses = (hoy.year - socio.fecha_inscripcion.year) * 12 + (hoy.month - socio.fecha_inscripcion.month)
    # Ajuste por día: si el día actual es mayor o igual al día de inscripción, ya pasó ese mes
    if hoy.day >= socio.fecha_inscripcion.day:
        meses += 1
    # Restamos 1 (el mes de alta ya pagado)
    return max(0, meses - 1)

def alta_socio(dni: str, nombre: str, telefono: str, direccion: str, email: str, membresia: str) -> str:
    """
    Da de alta un nuevo socio o reactiva si existe inactivo y debe menos de 2 cuotas.
    Retorna un mensaje informativo.
    """
    socio_existente = repositorio_socios.buscar_por_dni(dni)
    
    if socio_existente:
        if socio_existente.activo:
            return f"Ya existe un socio activo con DNI {dni}. No se puede dar de alta nuevamente."
        else:
            deuda = cuotas_adeudadas(socio_existente)
            if deuda >= 2:
                return f"El socio con DNI {dni} debe {deuda} cuotas. No se puede reactivar hasta regularizar (máximo 2 cuotas)."
            else:
                # Reactivar
                socio_existente.activo = True
                socio_existente.fecha_inscripcion = date.today()
                socio_existente.membresia = membresia  # Podría actualizar membresía también
                # Guardar cambios
                socios = repositorio_socios.cargar_socios()
                for i, s in enumerate(socios):
                    if s.numero_socio == socio_existente.numero_socio:
                        socios[i] = socio_existente
                        break
                repositorio_socios.guardar_socios(socios)
                return f"Socio {socio_existente.nombre_completo} reactivado correctamente. Número de socio: {socio_existente.numero_socio}"
    
    # Nuevo socio
    socios = repositorio_socios.cargar_socios()
    nuevo_numero = max([s.numero_socio for s in socios], default=0) + 1
    nuevo_socio = Socio(
        numero_socio=nuevo_numero,
        dni=dni,
        nombre_completo=nombre,
        telefono=telefono,
        direccion=direccion,
        email=email,
        membresia=membresia,
        fecha_inscripcion=date.today(),
        activo=True
    )
    socios.append(nuevo_socio)
    repositorio_socios.guardar_socios(socios)
    return f"Socio {nombre} registrado correctamente. Número de socio: {nuevo_numero}"

def reactivar_socio(identificador: str) -> str:
    """Reactivar socio por DNI o número de socio (como string)."""
    socio = None
    if identificador.isdigit():
        socio = repositorio_socios.buscar_por_numero(int(identificador))
    else:
        socio = repositorio_socios.buscar_por_dni(identificador)
    
    if not socio:
        return "Socio no encontrado."
    if socio.activo:
        return "El socio ya está activo."
    
    deuda = cuotas_adeudadas(socio)
    if deuda >= 2:
        return f"El socio debe {deuda} cuotas. No se puede reactivar hasta regularizar."
    
    socio.activo = True
    socio.fecha_inscripcion = date.today()
    socios = repositorio_socios.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socios.guardar_socios(socios)
    return f"Socio {socio.nombre_completo} reactivado correctamente. Nueva fecha de inscripción: {socio.fecha_inscripcion}"

def listar_socios(mostrar_inactivos: bool = False) -> List[Socio]:
    socios = repositorio_socios.cargar_socios()
    if mostrar_inactivos:
        return socios
    return [s for s in socios if s.activo]

def buscar_por_dni(dni: str) -> Optional[Socio]:
    return repositorio_socios.buscar_por_dni(dni)

def buscar_por_numero(numero: int) -> Optional[Socio]:
    return repositorio_socios.buscar_por_numero(numero)

def editar_socio(dni: str, nuevos_datos: dict) -> str:
    """
    Edita un socio existente. Permite cambiar: nombre_completo, telefono, direccion, email, membresia.
    No permite cambiar DNI, numero_socio, fecha_inscripcion ni activo.
    """
    socio = repositorio_socios.buscar_por_dni(dni)
    if not socio:
        return f"No se encontró socio con DNI {dni}."
    
    if "nombre_completo" in nuevos_datos:
        socio.nombre_completo = nuevos_datos["nombre_completo"]
    if "telefono" in nuevos_datos:
        socio.telefono = nuevos_datos["telefono"]
    if "direccion" in nuevos_datos:
        socio.direccion = nuevos_datos["direccion"]
    if "email" in nuevos_datos:
        socio.email = nuevos_datos["email"]
    if "membresia" in nuevos_datos:
        socio.membresia = nuevos_datos["membresia"]
    
    socios = repositorio_socios.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socios.guardar_socios(socios)
    return "Socio actualizado correctamente."

def eliminar_socio_logico(dni: str) -> str:
    socio = repositorio_socios.buscar_por_dni(dni)
    if not socio:
        return f"No se encontró socio con DNI {dni}."
    if not socio.activo:
        return "El socio ya estaba inactivo."
    socio.activo = False
    socios = repositorio_socios.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socios.guardar_socios(socios)
    return f"Socio {socio.nombre_completo} (DNI {dni}) marcado como inactivo."

def listar_morosos() -> List[Socio]:
    """Devuelve lista de socios activos que están morosos."""
    socios = listar_socios()
    return [s for s in socios if es_moroso(s)]