from typing import List, Optional
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from domain.socios import Socio
from persistence import repositorio_socios

DIAS_GRACIA = 10
COSTO_BASICA = 30.0
COSTO_PREMIUM = 50.0

def obtener_costo_mensual(membresia: str) -> float:
    if membresia == "premium":
        return COSTO_PREMIUM
    return COSTO_BASICA

def calcular_vencimiento(socio: Socio) -> date:
    base = socio.fin_cobertura if socio.fin_cobertura else socio.fecha_inscripcion
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

def obtener_detalle_reactivacion(socio, membresia_elegida=None):
    """
    Retorna un dict con:
    - meses: int (cantidad de meses que se pagan en total)
    - monto_total: float
    - observacion: str
    - extender_desde_fin_cobertura: bool (True = extiende desde fin_cobertura, False = desde hoy)
    - membresia_elegida: str
    - fecha_fin: date (nueva fecha de vencimiento calculada)
    """
    hoy = date.today()
    
    if socio.motivo_baja == "manual":
        # Reactivación voluntaria: 1 mes, cobertura desde hoy
        meses = 1
        if membresia_elegida is None:
            membresia_elegida = socio.membresia
        monto = obtener_costo_mensual(membresia_elegida) * meses
        observacion = f"Reactivación voluntaria - cuota {membresia_elegida}"
        extender_desde_fin_cobertura = False
        fecha_fin = hoy + relativedelta(months=1)
    
    else:  # mora
        if socio.fecha_baja is None:
            # Si por alguna razón no tiene fecha_baja, usamos una aproximación
            # pero idealmente siempre debería tenerla.
            fecha_baja = calcular_vencimiento(socio) + timedelta(days=DIAS_GRACIA)
        else:
            fecha_baja = socio.fecha_baja

        dias_transcurridos = (hoy - fecha_baja).days

        # Si transcurrieron 30 días o menos, consideramos que está dentro del mismo mes
        # y solo debe pagar 1 mes, corriendo la fecha de vencimiento.
        if dias_transcurridos <= 30:
            meses = 1
            membresia_elegida = socio.membresia  # forzamos la actual
            monto = obtener_costo_mensual(membresia_elegida) * meses
            observacion = f"Reactivación por mora (mismo mes) - cuota {membresia_elegida}"
            extender_desde_fin_cobertura = True   # CORRE desde la última cobertura
            # Calcular fecha_fin: fin_cobertura + 1 mes
            base = socio.fin_cobertura if socio.fin_cobertura else socio.fecha_inscripcion
            fecha_fin = base + relativedelta(months=1)
        else:
            # Pasó más de un mes: multa + cuota, cobertura desde hoy
            meses = 2
            membresia_actual = socio.membresia
            if membresia_elegida is None:
                membresia_elegida = socio.membresia
            monto = obtener_costo_mensual(membresia_actual) + obtener_costo_mensual(membresia_elegida)
            observacion = f"Reactivación por mora (multa {membresia_actual} - cuota {membresia_elegida})"
            extender_desde_fin_cobertura = False
            fecha_fin = hoy + relativedelta(months=1)  # cobertura real desde hoy

    return {
        "meses": meses,
        "monto_total": monto,
        "observacion": observacion,
        "extender_desde_fin_cobertura": extender_desde_fin_cobertura,
        "membresia_elegida": membresia_elegida,
        "fecha_fin": fecha_fin
    }

def _reactivar_socio(socio, nueva_membresia: str = None) -> str:
    if socio.activo:
        return "El socio ya está activo."

    detalle = obtener_detalle_reactivacion(socio, nueva_membresia)
    meses = detalle["meses"]
    monto_total = detalle["monto_total"]
    observacion = detalle["observacion"]
    extender_desde_fin_cobertura = detalle["extender_desde_fin_cobertura"]
    membresia_elegida = detalle["membresia_elegida"]

    # Actualizar membresía si cambia
    if membresia_elegida != socio.membresia:
        socio.membresia = membresia_elegida
        socio.fecha_cambio_membresia = date.today()

    # Calcular nueva fin_cobertura según el caso
    hoy = date.today()
    if extender_desde_fin_cobertura:
        base = socio.fin_cobertura if socio.fin_cobertura else socio.fecha_inscripcion
        nueva_fecha = base + relativedelta(months=1)  # corre un mes desde la anterior
    else:
        nueva_fecha = hoy + relativedelta(months=1)   # desde hoy

    socio.fin_cobertura = nueva_fecha
    socio.activo = True
    socio.motivo_baja = None
    socio.fecha_baja = None  # limpiamos la fecha de baja

    if not repositorio_socios.actualizar_socio(socio):
        return "Error al actualizar el socio."

    from services.gestor_pagos import registrar_pago_automatico
    registrar_pago_automatico(
        socio.numero_socio,
        meses,
        monto_total,
        membresia_elegida,
        observacion
    )

    return (f"Socio {socio.nombre_completo} reactivado. Pago de {meses} mes(es) por ${monto_total:.2f}, "
            f"cobertura hasta {socio.fin_cobertura.strftime('%d/%m/%Y')}.")

def reactivar_socio(identificador: str, nueva_membresia: str = None) -> str:
    socio = buscar_por_identificador(identificador)
    if not socio:
        return "Socio no encontrado."
    if socio.activo:
        return "El socio ya está activo."
    return _reactivar_socio(socio, nueva_membresia)

def alta_socio(dni: str, nombre: str, telefono: str, direccion: str, email: str, membresia: str) -> str:
    socio_existente = repositorio_socios.buscar_por_dni(dni)
    if socio_existente:
        if socio_existente.activo:
            return f"Ya existe un socio activo con DNI {dni}."
        else:
            return f"DNI {dni} pertenece a un socio inactivo. Por favor, reactívelo desde el menú de reactivación."
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
        fin_cobertura=date.today() + relativedelta(months=1),
        activo=True,
        motivo_baja=None,
        fecha_baja=None
    )
    socios.append(nuevo_socio)
    repositorio_socios.guardar_socios(socios)

    from services.gestor_pagos import registrar_pago_automatico
    costo_mensual = obtener_costo_mensual(membresia)
    registrar_pago_automatico(
        nuevo_numero,
        1,
        costo_mensual,
        membresia,
        "Pago de alta"
    )
    return f"Socio {nombre} registrado. Cobertura hasta {nuevo_socio.fin_cobertura.strftime('%d/%m/%Y')}."

def aplicar_baja_automatica():
    socios = repositorio_socios.cargar_socios()
    cambios = False
    hoy = date.today()
    for s in socios:
        if s.activo and dias_desde_vencimiento(s) > DIAS_GRACIA:
            s.activo = False
            s.motivo_baja = "mora"
            s.fecha_baja = hoy   # registramos la fecha de desactivación
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
    estado = obtener_estado(socio)
    if estado in ("debe_cuota", "inactivo_por_deuda"):
        return "El socio está en período de gracia o adeuda cuotas. Debe pagar deuda."
    if not socio.activo:
        return "El socio ya estaba inactivo."
    socio.activo = False
    socio.motivo_baja = "manual"
    socio.fecha_baja = date.today()
    if repositorio_socios.actualizar_socio(socio):
        return f"Socio {socio.nombre_completo} (DNI {socio.dni}) marcado como inactivo (baja manual)."
    else:
        return "Error al actualizar el socio."

def obtener_detalle_socio(identificador: str) -> Optional[Socio]:
    return buscar_por_identificador(identificador)

def editar_actividades_socio(identificador: str, nuevas_actividades: list) -> str:
    socio = buscar_por_identificador(identificador)
    if not socio:
        return f"No se encontró socio con identificador {identificador}."
    socio.actividades = nuevas_actividades
    if repositorio_socios.actualizar_socio(socio):
        return "Actividades del socio actualizadas correctamente."
    else:
        return "Error al actualizar las actividades del socio."