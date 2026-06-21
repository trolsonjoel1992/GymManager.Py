def mostrar_submenu():
    while True:
        print("\n--- ESTADÍSTICAS Y REPORTES ---")
        print("1. Concurrencia total por actividad (últimos 30 días)")
        print("2. Actividad con mayor y menor concurrencia")
        print("3. Porcentaje de asistencia de un socio")
        print("4. Cantidad de socios activos vs morosos")
        print("5. Reporte de ingresos mensuales")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            concurrencia_actividad()
        elif opcion == "2":
            ranking_actividades()
        elif opcion == "3":
            porcentaje_asistencia()
        elif opcion == "4":
            activos_vs_morosos()
        elif opcion == "5":
            reporte_ingresos()
        elif opcion == "6":
            break
        else:
            print("Opción no válida.")

def concurrencia_actividad():
    print("\n[Concurrencia por actividad - últimos 30 días] (Funcionalidad en desarrollo)")

def ranking_actividades():
    print("\n[Ranking de actividades] (Funcionalidad en desarrollo)")

def porcentaje_asistencia():
    dni = input("DNI del socio: ")
    print(f"\n[Porcentaje de asistencia de {dni}] (Funcionalidad en desarrollo)")

def activos_vs_morosos():
    print("\n[Gráfico de activos vs morosos] (Funcionalidad en desarrollo)")

def reporte_ingresos():
    mes = input("Mes (1-12): ")
    anio = input("Año: ")
    print(f"\n[Reporte de ingresos para {mes}/{anio}] (Funcionalidad en desarrollo)")