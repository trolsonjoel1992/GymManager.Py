from datetime import date, timedelta
from typing import List, Optional
from domain.pagos import Pago
from persistence import repositorio_pago, repositorio_socio

def registrar_pago_automatico(numero_socio: int, meses: int = 1, observacion: str = "") -> Pago:
    """Registra un pago automático (sin monto específico) al dar de alta o reactivar."""
    pagos = repositorio_pago.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    pago = Pago(
        id=nuevo_id,
        numero_socio=numero_socio,
        fecha_pago=date.today(),
        monto=0.0,      # No se registra monto en altas automáticas
        meses_cubiertos=meses,
        observaciones=observacion
    )
    repositorio_pago.agregar_pago(pago)
    return pago

def registrar_pago(dni: str, monto: float, meses: int = 1) -> str:
    """Registra un pago manual desde el menú de pagos."""
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo. No se puede registrar pago."
    
    # Actualizar fecha_ultimo_pago en el socio
    if socio.fecha_ultimo_pago is None:
        socio.fecha_ultimo_pago = date.today()
    else:
        # Sumar los meses pagados a partir de hoy (pago adelantado)
        socio.fecha_ultimo_pago = date.today() + timedelta(days=(meses-1)*30)
    
    # Guardar socio
    socios = repositorio_socio.cargar_socios()
    for i, s in enumerate(socios):
        if s.numero_socio == socio.numero_socio:
            socios[i] = socio
            break
    repositorio_socio.guardar_socios(socios)
    
    # Registrar pago en historial
    pagos = repositorio_pago.cargar_pagos()
    nuevo_id = max([p.id for p in pagos], default=0) + 1
    pago = Pago(
        id=nuevo_id,
        numero_socio=socio.numero_socio,
        fecha_pago=date.today(),
        monto=monto,
        meses_cubiertos=meses,
        observaciones=f"Pago de {meses} mes(es)"
    )
    repositorio_pago.agregar_pago(pago)
    
    return f"Pago de ${monto} registrado por {meses} mes(es). El socio {socio.nombre_completo} está al día hasta {socio.fecha_vencimiento(meses)}."

def obtener_historial_pagos(dni: str) -> List[Pago]:
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return []
    return repositorio_pago.obtener_pagos_por_socio(socio.numero_socio)

def obtener_ultimo_pago(dni: str) -> Optional[Pago]:
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return None
    return repositorio_pago.obtener_ultimo_pago(socio.numero_socio)

def mostrar_estado_cuotas(dni: str) -> str:
    """Muestra información del estado de cuotas de un socio."""
    socio = repositorio_socio.buscar_por_dni(dni)
    if not socio:
        return "Socio no encontrado."
    if not socio.activo:
        return "El socio está inactivo."
    from services.gestor_socios import obtener_estado
    estado = obtener_estado(socio)
    venc = socio.fecha_vencimiento()
    if estado == "activo":
        dias_restantes = (venc - date.today()).days
        return f"Estado: ACTIVO. Próximo vencimiento: {venc} (faltan {dias_restantes} días)."
    elif estado == "debe_cuota":
        dias_atraso = (date.today() - venc).days
        return f"Estado: DEBE CUOTA. Vencimiento: {venc} (hace {dias_atraso} días)."
    else:
        return "Estado: INACTIVO (más de 2 meses sin pagar)."