from datetime import date
from typing import List, Optional
from dateutil.relativedelta import relativedelta
from domain.pagos import Pago
from persistence import repositorio_pagos, repositorio_socios
from services import gestor_inscripciones, gestor_socios

def registrar_pago_automatico(
    numero_socio: int, meses: int, monto: float, membresia: str, observacion: str
) -> Pago:
    pagos = repositorio_pagos.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    pago = Pago(
        id=nuevo_id,
        numero_socio=numero_socio,
        fecha_pago=date.today(),
        monto=monto,
        meses_cubiertos=meses,
        membresia=membresia,
        observaciones=observacion,
    )
    repositorio_pagos.agregar_pago(pago)
    return pago

def registrar_pago(
    dni: str, monto: float, meses: int, nueva_membresia: Optional[str] = None
) -> str:
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo. No se puede registrar pago."
    if nueva_membresia and nueva_membresia != socio.membresia:
        if nueva_membresia == "premium":
            observacion = "Cambio a Premium"
        else:
            observacion = "Downgrade a Básica"
        socio.membresia = nueva_membresia
        socio.fecha_cambio_membresia = date.today()
        membresia_abonada = nueva_membresia
    else:
        observacion = f"Pago de {meses} mes(es)"
        membresia_abonada = socio.membresia
    hoy = date.today()
    if socio.fin_cobertura is None:
        nueva_fecha = hoy + relativedelta(months=meses)
    else:
        nueva_fecha = socio.fin_cobertura + relativedelta(months=meses)
        if nueva_fecha < hoy:
            nueva_fecha = hoy + relativedelta(months=meses)
    socio.fin_cobertura = nueva_fecha
    if not repositorio_socios.actualizar_socio(socio):
        return "Error al actualizar el socio."
    pagos = repositorio_pagos.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    pago = Pago(
        id=nuevo_id,
        numero_socio=socio.numero_socio,
        fecha_pago=hoy,
        monto=monto,
        meses_cubiertos=meses,
        membresia=membresia_abonada,
        observaciones=observacion,
    )
    repositorio_pagos.agregar_pago(pago)
    gestor_inscripciones.extender_inscripciones(socio.numero_socio, nueva_fecha)
    mensaje = f"Pago de ${monto} registrado. Cobertura extendida hasta {nueva_fecha.strftime('%d/%m/%Y')}."
    if nueva_membresia:
        mensaje += f" Membresía actualizada a {nueva_membresia.upper()}."
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
    return repositorio_pagos.obtener_pagos_por_socio(socio.numero_socio)

def obtener_ultimo_pago(dni: str) -> Optional[Pago]:
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        return None
    return repositorio_pagos.obtener_ultimo_pago(socio.numero_socio)

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