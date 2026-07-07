from services import gestor_estadisticas, gestor_socios
from utils.inputs import input_int, input_str

def mostrar_submenu():
    while True:
        print("\n--- ESTADÍSTICAS Y REPORTES ---")
        print("1. Concurrencia total por actividad (últimos 30 días)")
        print("2. Actividad con mayor y menor concurrencia")
        print("3. Porcentaje de asistencia de un socio")
        print("4. Cantidad de socios activos vs morosos")
        print("5. Reporte de ingresos mensuales")
        print("6. Volver al menú principal")
        opcion = input_int("Seleccione una opción: ", min=1, max=6)
        if opcion == 1:
            concurrencia_actividad()
        elif opcion == 2:
            ranking_actividades()
        elif opcion == 3:
            porcentaje_asistencia()
        elif opcion == 4:
            activos_vs_morosos()
        elif opcion == 5:
            reporte_ingresos()
        elif opcion == 6:
            break

def concurrencia_actividad():
    print("\n--- Concurrencia por actividad (últimos 30 días) ---")
    datos = gestor_estadisticas.concurrencia_por_actividad()
    if not datos:
        print("No hay asistencias registradas en el período.")
        return
    for nombre, cantidad in datos.items():
        print(f"{nombre}: {cantidad} asistencias")

def ranking_actividades():
    print("\n--- Actividad con mayor y menor concurrencia ---")
    mas_nom, mas_cant, menos_nom, menos_cant = gestor_estadisticas.actividad_mas_y_menos_concurrida()
    if mas_cant == 0:
        print("No hay datos de concurrencia.")
        return
    print(f"Mayor concurrencia: {mas_nom} ({mas_cant} asistencias)")
    print(f"Menor concurrencia: {menos_nom} ({menos_cant} asistencias)")

def porcentaje_asistencia():
    identificador = input_str("DNI o número de socio: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    porcentaje = gestor_estadisticas.porcentaje_asistencia_socio(socio.numero_socio)
    print(f"\nPorcentaje de asistencia de {socio.nombre_completo}: {porcentaje}%")

def activos_vs_morosos():
    print("\n--- Resumen de estado de socios ---")
    resumen = gestor_estadisticas.resumen_estado_socios()
    print(f"Activos al día: {resumen['activos_al_dia']}")
    print(f"Morosos (período de gracia): {resumen['morosos']}")
    print(f"Inactivos por deuda: {resumen['inactivos_por_deuda']}")
    print(f"Inactivos por baja manual: {resumen['inactivos_manual']}")

def reporte_ingresos():
    mes = input_int("Mes (1-12): ", min=1, max=12)
    anio = input_int("Año: ")
    ingresos = gestor_estadisticas.ingresos_mensuales(mes, anio)
    print(f"\n--- Ingresos del mes {mes}/{anio} ---")
    print(f"Total recaudado: ${ingresos['total']}")
    print(f"  Membresía Básica: ${ingresos['basica']}")
    print(f"  Membresía Premium: ${ingresos['premium']}")