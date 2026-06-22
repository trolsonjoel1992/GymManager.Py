from typing import List, Optional
from datetime import date, timedelta
from domain.socios import Socio
from persistence import repositorio_socio

DIAS_DEUDA = 30      # Pasado 1 mes, debe cuota
DIAS_INACTIVO = 45   # Pasado 2 meses, inactivo automático

def dias_vencidos(socio: Socio) -> int:
    """Días transcurridos desde la fecha de inscripción (último pago)."""
    hoy = date.today()
    return (hoy - socio.fecha_inscripcion).days

def obtener_estado(socio: Socio) -> str:
    """
    Retorna el estado del socio según la cantidad de días desde su última fecha de pago.
    - 'activo': menos de 30 días.
    - 'debe_cuota': entre 30 y 44 días.
    - 'inactivo': 45 días o más, o si socio.activo es False.
    """
    if not socio.activo:
        return "inactivo"
    dias = dias_vencidos(socio)
    if dias < DIAS_DEUDA:
        return "activo"
    elif dias < DIAS_INACTIVO:
        return "debe_cuota"
    else:
        return "inactivo"

def es_moroso(socio: Socio) -> bool:
    return obtener_estado(socio) == "debe_cuota"

def esta_inactivo(socio: Socio) -> bool:
    return obtener_estado(socio) == "inactivo"

def puede_inscribirse(socio: Socio) -> bool:
    return not esta_inactivo(socio)

def puede_tomar_asistencia(socio: Socio) -> bool:
    return not esta_inactivo(socio)

def alta_socio(dni: str, nombre: str, telefono: str, direccion: str, email: str, membresia: str) -> str:
    socio_existente = repositorio_socio.buscar_por_dni(dni)
    
    if socio_existente:
        if socio_existente.activo:
            return f"Ya existe un socio activo con DNI {dni}."
        else:
            estado = obtener_estado(socio_existente)
            if estado == "debe_cuota":
                return f"El socio con DNI {dni} debe una cuota. No se puede reactivar hasta regularizar."
            else:
                # Reactivar: se pone activo, se actualiza fecha_ultimo_pago y se registra el pago
                socio_existente.activo = True
                socio_existente.fecha_ultimo_pago = date.today()
                socio_existente.membresia = membresia
                socios = repositorio_socio.cargar_socios()
                for i, s in enumerate(socios):
                    if s.numero_socio == socio_existente.numero_socio:
                        socios[i] = socio_existente
                        break
                repositorio_socio.guardar_socios(socios)
                # Registrar pago automático (importación local para evitar circular)
                from services.gestor_pagos import registrar_pago_automatico
                registrar_pago_automatico(socio_existente.numero_socio, 1, "Pago de reactivación")
                return f"Socio {socio_existente.nombre_completo} reactivado correctamente. Número de socio: {socio_existente.numero_socio}"
    
    # Nuevo socio
    socios = repositorio_socio.cargar_socios()
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
        fecha_ultimo_pago=date.today(),
        activo=True
    )
    socios.append(nuevo_socio)
    repositorio_socio.guardar_socios(socios)
    # Registrar pago automático (importación local para evitar circular)
    from services.gestor_pagos import registrar_pago_automatico
    registrar_pago_automatico(nuevo_numero, 1, "Pago de alta")
    return f"Socio {nombre} registrado correctamente. Número de socio: {nuevo_numero}"

def reactivar_socio(identificador: str) -> str:
    socio = None
    if identificador.isdigit():
        socio = repositorio_socio.buscar_por_numero(int(identificador))
    else:
        socio = repositorio_socio.buscar_por_dni(identificador)
    
    if not socio:
        return "Socio no encontrado."
    if socio.activo:
        return "El socio ya está activo."
    
    estado = obtener_estado(socio)
    if estado == "debe_cuota":
        return f"El socio debe una cuota. No se puede reactivar hasta regularizar."
    elif estado == "inactivo":
        socio.activo = True
        socio.fecha_inscripcion = date.today()
        socios = repositorio_socio.cargar_socios()
        for i, s in enumerate(socios):
            if s.numero_socio == socio.numero_socio:
                socios[i] = socio
                break
        repositorio_socio.guardar_socios(socios)
        return f"Socio {socio.nombre_completo} reactivado correctamente."
    else:
        return "El socio ya está activo."

def registrar_pago(dni: str, monto: float) -> str:
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo. No se puede registrar pago."
    socio.fecha_ultimo_pago = date.today()
    socios = repositorio_socio.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socio.guardar_socios(socios)
    return f"Pago de ${monto} registrado. El socio {socio.nombre_completo} está al día."

def listar_socios(mostrar_inactivos: bool = False) -> List[Socio]:
    socios = repositorio_socio.cargar_socios()
    if mostrar_inactivos:
        return socios
    return [s for s in socios if s.activo]

def buscar_por_dni(dni: str) -> Optional[Socio]:
    return repositorio_socio.buscar_por_dni(dni)

def buscar_por_numero(numero: int) -> Optional[Socio]:
    return repositorio_socio.buscar_por_numero(numero)

def editar_socio(dni: str, nuevos_datos: dict) -> str:
    socio = repositorio_socio.buscar_por_dni(dni)
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
    socios = repositorio_socio.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socio.guardar_socios(socios)
    return "Socio actualizado correctamente."

def eliminar_socio_logico(dni: str) -> str:
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return f"No se encontró socio con DNI {dni}."
    if not socio.activo:
        return "El socio ya estaba inactivo."
    socio.activo = False
    socios = repositorio_socio.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socio.guardar_socios(socios)
    return f"Socio {socio.nombre_completo} (DNI {dni}) marcado como inactivo."

def listar_morosos() -> List[Socio]:
    socios = listar_socios()
    return [s for s in socios if es_moroso(s)]

def aplicar_baja_automatica():
    """Pone inactivos a los socios que superan los 45 días sin pagar."""
    socios = repositorio_socio.cargar_socios()
    cambios = False
    for s in socios:
        if s.activo and obtener_estado(s) == "inactivo":
            s.activo = False
            cambios = True
    if cambios:
        repositorio_socio.guardar_socios(socios)