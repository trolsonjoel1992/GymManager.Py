from datetime import date, timedelta
from typing import Dict, Tuple
from persistence import repositorio_asistencias as repo_asist
from persistence import repositorio_pagos as repo_pagos
from persistence import repositorio_socios as repo_socios
from services import gestor_actividades, gestor_socios

def concurrencia_por_actividad(dias: int = 30) -> Dict[str, int]:
    """Retorna un dict {nombre_actividad: cantidad_de_presentes} en los últimos N días."""
    desde = date.today() - timedelta(days=dias)
    asistencias = repo_asist.obtener_todas()
    conteo = {}
    for a in asistencias:
        if a.fecha >= desde and a.presente:
            act = gestor_actividades.obtener_actividad(a.id_actividad)
            nombre = act.nombre if act else f"Actividad {a.id_actividad}"
            conteo[nombre] = conteo.get(nombre, 0) + 1
    return dict(sorted(conteo.items(), key=lambda x: x[1], reverse=True))

def actividad_mas_y_menos_concurrida(dias: int = 30) -> Tuple[str, int, str, int]:
    """Retorna (nombre_mas, conteo_mas, nombre_menos, conteo_menos)."""
    conteo = concurrencia_por_actividad(dias)
    if not conteo:
        return ("Sin datos", 0, "Sin datos", 0)
    items = list(conteo.items())
    max_item = max(items, key=lambda x: x[1])
    min_item = min(items, key=lambda x: x[1])
    return max_item[0], max_item[1], min_item[0], min_item[1]

def porcentaje_asistencia_socio(numero_socio: int) -> float:
    """Retorna el porcentaje de asistencia (presentes / total) de un socio."""
    asistencias = repo_asist.obtener_por_socio(numero_socio)
    total = len(asistencias)
    if total == 0:
        return 0.0
    presentes = sum(1 for a in asistencias if a.presente)
    return round((presentes / total) * 100, 2)

def resumen_estado_socios() -> Dict[str, int]:
    """
    Retorna un dict con:
    - activos_al_dia
    - morosos (periodo de gracia)
    - inactivos_por_deuda
    - inactivos_manual
    """
    todos = repo_socios.cargar_socios()
    resultado = {
        "activos_al_dia": 0,
        "morosos": 0,
        "inactivos_por_deuda": 0,
        "inactivos_manual": 0,
    }
    for s in todos:
        estado = gestor_socios.obtener_estado(s)
        if estado == "activo":
            resultado["activos_al_dia"] += 1
        elif estado == "debe_cuota":
            resultado["morosos"] += 1
        elif estado == "inactivo_por_deuda":
            resultado["inactivos_por_deuda"] += 1
        elif estado == "inactivo":
            resultado["inactivos_manual"] += 1
    return resultado

def ingresos_mensuales(mes: int, anio: int) -> Dict[str, float]:
    """Retorna el total recaudado en un mes y el desglose por membresía."""
    pagos = repo_pagos.cargar_pagos()
    total = 0.0
    total_basica = 0.0
    total_premium = 0.0
    for p in pagos:
        if p.fecha_pago.year == anio and p.fecha_pago.month == mes:
            total += p.monto
            if p.membresia == "basica":
                total_basica += p.monto
            else:
                total_premium += p.monto
    return {
        "total": round(total, 2),
        "basica": round(total_basica, 2),
        "premium": round(total_premium, 2),
    }