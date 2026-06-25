from typing import List, Optional
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from domain.socios import Socio
from persistence import repositorio_socios

DIAS_GRACIA = 10   # días de gracia después del vencimiento

# Costos mensuales por membresía
COSTO_MENSUAL_BASICA = 30.0   # ajusta según tu negocio
COSTO_MENSUAL_PREMIUM = 50.0

def obtener_costo_mensual(membresia: str) -> float:
    """Retorna el costo mensual según el tipo de membresía."""
    if membresia == "premium":
        return COSTO_MENSUAL_PREMIUM
    return COSTO_MENSUAL_BASICA

def calcular_vencimiento(socio: Socio) -> date:
    base = socio.fecha_ultimo_pago if socio.fecha_ultimo_pago else socio.fecha_inscripcion
    return base + relativedelta(months=1)

def dias_desde_vencimiento(socio: Socio) -> int:
    venc = calcular_vencimiento(socio)
    hoy = date.today()
    return (hoy - venc).days

def obtener_estado(socio: Socio) -> str:
    if not socio.activo:
        if socio.motivo_baja == "mora":
            return "inactivo_por_deuda"
        else:
            return "inactivo"
    dias = dias_desde_vencimiento(socio)
    if dias <= 0:
        return "activo"
    elif dias <= DIAS_GRACIA:
        return "debe_cuota"
    else:
        return "inactivo_por_deuda"

def es_moroso(socio: Socio) -> bool:
    return obtener_estado(socio) == "debe_cuota"

def esta_inactivo(socio: Socio) -> bool:
    return obtener_estado(socio) in ("inactivo", "inactivo_por_deuda")

def buscar_por_identificador(identificador: str) -> Optional[Socio]:
    if not identificador:
        return None
    if identificador.isdigit():
        socio = repositorio_socios.buscar_por_numero(int(identificador))
        if socio:
            return socio
    return repositorio_socios.buscar_por_dni(identificador)

def calcular_meses_reactivacion(socio: Socio) -> int:
    if socio.motivo_baja == "manual":
        return 1
    venc = calcular_vencimiento(socio)
    fecha_baja = venc + timedelta(days=DIAS_GRACIA)
    hoy = date.today()
    if fecha_baja.year == hoy.year and fecha_baja.month == hoy.month:
        return 1
    else:
        return 2

def _reactivar_socio(socio: Socio, pago_meses: int = None, nueva_membresia: str = None) -> str:
    if socio.activo:
        return "El socio ya está activo."

    if pago_meses is None:
        pago_meses = calcular_meses_reactivacion(socio)

    membresia_para_pago = nueva_membresia if nueva_membresia else socio.membresia
    costo_mensual = obtener_costo_mensual(membresia_para_pago)
    monto_total = costo_mensual * pago_meses

    if nueva_membresia and nueva_membresia != socio.membresia:
        socio.membresia = nueva_membresia

    socio.activo = True
    socio.motivo_baja = None
    socio.fecha_ultimo_pago = date.today() + relativedelta(months=1)

    if not repositorio_socios.actualizar_socio(socio):
        return "Error al actualizar el socio."

    from services.gestor_pagos import registrar_pago_automatico
    registrar_pago_automatico(
        socio.numero_socio,
        pago_meses,
        monto_total,
        membresia_para_pago,   # <--- PASAMOS LA MEMBRESÍA
        "Pago reactivación"
    )

    if pago_meses == 1:
        extension = "se extiende la cobertura por 1 mes"
    else:
        extension = "se pagan 2 meses pero la cobertura se extiende solo 1 mes (el segundo es multa)"
    return (f"Socio {socio.nombre_completo} reactivado. Pago de {pago_meses} mes(es) por ${monto_total:.2f}, "
            f"{extension} hasta {socio.fecha_ultimo_pago.strftime('%d/%m/%Y')}.")

def reactivar_socio(identificador: str, pago_meses: int = None, nueva_membresia: str = None) -> str:
    socio = buscar_por_identificador(identificador)
    if not socio:
        return "Socio no encontrado."
    if socio.activo:
        return "El socio ya está activo."
    return _reactivar_socio(socio, pago_meses, nueva_membresia)

def alta_socio(dni: str, nombre: str, telefono: str, direccion: str, email: str, membresia: str) -> str:
    socio_existente = repositorio_socios.buscar_por_dni(dni)
    if socio_existente:
        if socio_existente.activo:
            return f"Ya existe un socio activo con DNI {dni}."
        else:
            return _reactivar_socio(socio_existente)

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
        fecha_ultimo_pago=date.today() + relativedelta(months=1),
        activo=True,
        motivo_baja=None
    )
    socios.append(nuevo_socio)
    repositorio_socios.guardar_socios(socios)

    from services.gestor_pagos import registrar_pago_automatico
    costo_mensual = obtener_costo_mensual(membresia)
    registrar_pago_automatico(
        nuevo_numero,
        1,
        costo_mensual,
        membresia,   # <--- PASAMOS LA MEMBRESÍA
        "Pago de alta"
    )
    return f"Socio {nombre} registrado. Cobertura hasta {nuevo_socio.fecha_ultimo_pago.strftime('%d/%m/%Y')}."

def aplicar_baja_automatica():
    socios = repositorio_socios.cargar_socios()
    cambios = False
    for s in socios:
        if s.activo and dias_desde_vencimiento(s) > DIAS_GRACIA:
            s.activo = False
            s.motivo_baja = "mora"
            cambios = True
    if cambios:
        repositorio_socios.guardar_socios(socios)

def listar_socios(mostrar_inactivos: bool = False) -> List[Socio]:
    socios = repositorio_socios.cargar_socios()
    if mostrar_inactivos:
        return socios
    return [s for s in socios if s.activo]

def listar_socios_activos() -> List[Socio]:
    return [s for s in repositorio_socios.cargar_socios() if s.activo]

def listar_socios_inactivos() -> List[Socio]:
    return [s for s in repositorio_socios.cargar_socios() if not s.activo]

def listar_morosos() -> List[Socio]:
    socios = listar_socios_activos()
    return [s for s in socios if es_moroso(s)]

def buscar_por_dni(dni: str) -> Optional[Socio]:
    return repositorio_socios.buscar_por_dni(dni)

def buscar_por_numero(numero: int) -> Optional[Socio]:
    return repositorio_socios.buscar_por_numero(numero)

def editar_socio(identificador: str, nuevos_datos: dict) -> str:
    socio = buscar_por_identificador(identificador)
    if not socio:
        return f"No se encontró socio con identificador {identificador}."
    if "membresia" in nuevos_datos:
        return "No se permite cambiar la membresía desde edición de socio. Use el módulo de pagos."
    if "nombre_completo" in nuevos_datos:
        socio.nombre_completo = nuevos_datos["nombre_completo"]
    if "telefono" in nuevos_datos:
        socio.telefono = nuevos_datos["telefono"]
    if "direccion" in nuevos_datos:
        socio.direccion = nuevos_datos["direccion"]
    if "email" in nuevos_datos:
        socio.email = nuevos_datos["email"]
    if repositorio_socios.actualizar_socio(socio):
        return "Socio actualizado correctamente."
    else:
        return "Error al actualizar el socio."

def eliminar_socio_logico(identificador: str) -> str:
    socio = buscar_por_identificador(identificador)
    if not socio:
        return f"No se encontró socio con identificador {identificador}."
    if not socio.activo:
        return "El socio ya estaba inactivo."
    socio.activo = False
    socio.motivo_baja = "manual"
    if repositorio_socios.actualizar_socio(socio):
        return f"Socio {socio.nombre_completo} (DNI {socio.dni}) marcado como inactivo (baja manual)."
    else:
        return "Error al actualizar el socio."

def obtener_detalle_socio(identificador: str) -> Optional[Socio]:
    return buscar_por_identificador(identificador)