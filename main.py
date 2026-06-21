# main.py
from ui import menu_socios
from ui import menu_actividades
from ui import menu_inscripciones
from ui import menu_asistencias
from ui import menu_pagos
from ui import menu_estadisticas

def mostrar_menu_principal():
    print("\n" + "="*50)
    print("         GESTOR DE GIMNASIO - ADMINISTRACIÓN")
    print("="*50)
    print("1. Gestión de Socios")
    print("2. Gestión de Actividades (predefinidas)")
    print("3. Inscripciones a Actividades")
    print("4. Control de Asistencia")
    print("5. Pagos y Control de Morosidad")
    print("6. Estadísticas y Reportes")
    print("7. Salir")
    print("="*50)

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            menu_socios.mostrar_submenu()
        elif opcion == "2":
            menu_actividades.mostrar_submenu()
        elif opcion == "3":
            menu_inscripciones.mostrar_submenu()
        elif opcion == "4":
            menu_asistencias.mostrar_submenu()
        elif opcion == "5":
            menu_pagos.mostrar_submenu()
        elif opcion == "6":
            menu_estadisticas.mostrar_submenu()
        elif opcion == "7":
            print("\n¡Hasta luego! Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()