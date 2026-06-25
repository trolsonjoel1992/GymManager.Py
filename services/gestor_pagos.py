from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List, Optional
from domain.pagos import Pago
from persistence import repositorio_pagos as repositorio_pago
from persistence import repositorio_socios
from services import gestor_socios

def registrar_pago_automatico(numero_socio: int, meses: int, monto: float, membresia: str, observacion: str = "") -> Pago:
    pagos = repositorio_pago.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    pago = Pago(
        id=nuevo_id,
        numero_socio=numero_socio,
        fecha_pago=date.today(),
        monto=monto,
        meses_cubiertos=meses,
        membresia=membresia,
        observaciones=observacion
    )
    repositorio_pago.agregar_pago(pago)
    return pago

def registrar_pago(dni: str, monto: float, meses: int = 1, nueva_membresia: Optional[str] = None) -> str:
    """
    Registra un pago manual para un socio activo.
    Si se proporciona nueva_membresia, debe ser "premium" y solo si el socio es "basica".
    El monto se calcula con el costo de la nueva membresía (si se cambia).
    Actualiza la fecha de último pago, membresía si corresponde, y guarda el registro.
    """
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo. No se puede registrar pago."

    membresia_actual = socio.membresia
    membresia_a_registrar = membresia_actual  # por defecto

    if nueva_membresia:
        if nueva_membresia != "premium":
            return "Solo se permite cambio a membresía Premium."
        if membresia_actual == "premium":
            return "El socio ya es Premium, no puede cambiar a Premium nuevamente."
        # Cambiar membresía
        socio.membresia = "premium"
        socio.fecha_cambio_membresia = date.today()
        membresia_a_registrar = "premium"   # registramos la nueva membresía en el pago
    else:
        # No hay cambio, registramos la actual
        membresia_a_registrar = membresia_actual

    hoy = date.today()
    if socio.fecha_ultimo_pago is None:
        nueva_fecha = hoy + relativedelta(months=meses)
    else:
        nueva_fecha = socio.fecha_ultimo_pago + relativedelta(months=meses)
        if nueva_fecha < hoy:
            nueva_fecha = hoy + relativedelta(months=meses)
    socio.fecha_ultimo_pago = nueva_fecha

    if not repositorio_socios.actualizar_socio(socio):
        return "Error al actualizar el socio."

    pagos = repositorio_pago.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    observacion = f"Pago de {meses} mes(es)"
    if nueva_membresia:
        observacion += " (cambio a Premium)"
    pago = Pago(
        id=nuevo_id,
        numero_socio=socio.numero_socio,
        fecha_pago=hoy,
        monto=monto,
        meses_cubiertos=meses,
        membresia=membresia_a_registrar,
        observaciones=observacion
    )
    repositorio_pago.agregar_pago(pago)

    mensaje = f"Pago de ${monto} registrado. Cobertura extendida hasta {nueva_fecha.strftime('%d/%m/%Y')}."
    if nueva_membresia:
        mensaje += " Membresía actualizada a Premium."
    return mensaje

def obtener_historial_pagos(identificador: str, tipo_busqueda: str = "dni") -> List[Pago]:
    socio = None
    if tipo_busqueda == "dni":
        socio = gestor_socios.buscar_por_dni(identificador)
    elif tipo_busqueda == "numero":
        try:
            numero = int(identificador)
            socio = gestor_socios.buscar_por_numero(numero)
        except ValueError:
            return []
    else:
        return []

    if not socio:
        return []
    return repositorio_pago.obtener_pagos_por_socio(socio.numero_socio)

def obtener_ultimo_pago(dni: str) -> Optional[Pago]:
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        return None
    return repositorio_pago.obtener_ultimo_pago(socio.numero_socio)

def obtener_estado_cuotas(identificador: str, tipo_busqueda: str = "dni") -> str:
    socio = None
    if tipo_busqueda == "dni":
        socio = gestor_socios.buscar_por_dni(identificador)
    elif tipo_busqueda == "numero":
        try:
            numero = int(identificador)
            socio = gestor_socios.buscar_por_numero(numero)
        except ValueError:
            return "Número de socio inválido."
    else:
        return "Tipo de búsqueda no válido."

    if not socio:
        return "Socio no encontrado."

    estado = gestor_socios.obtener_estado(socio)
    venc = gestor_socios.calcular_vencimiento(socio)
    hoy = date.today()
    dias = (hoy - venc).days

    if estado == "activo":
        if venc >= hoy:
            dias_restantes = (venc - hoy).days
            return f"Estado: ACTIVO (AL DÍA). Próximo vencimiento: {venc.strftime('%d/%m/%Y')} (faltan {dias_restantes} días)."
        else:
            return f"Estado: ACTIVO (AL DÍA). Vencimiento: {venc.strftime('%d/%m/%Y')}."
    elif estado == "debe_cuota":
        return f"Estado: MOROSO (período de gracia). Vencimiento: {venc.strftime('%d/%m/%Y')} (hace {dias} días). Debe pagar antes de que finalice el período de gracia."
    elif estado == "inactivo_por_deuda":
        return f"Estado: INACTIVO POR DEUDA. Vencimiento: {venc.strftime('%d/%m/%Y')} (hace {dias} días). El socio fue desactivado automáticamente por falta de pago."
    elif estado == "inactivo":
        return "Estado: INACTIVO (baja manual)."
    else:
        return "Estado desconocido."