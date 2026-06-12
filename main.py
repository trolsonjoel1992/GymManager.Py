from ui import menu_socios

def mostrar_menu():
    print("\n=== GESTOR DE GIMNASIO - SOCIOS ===")
    print("1. Agregar socio")
    print("2. Listar socios activos")
    print("3. Editar socio")
    print("4. Eliminar socio (baja lógica)")
    print("5. Salir")

def main():
    opciones = {
        "1": menu_socios.agregar_socio_interactivo,
        "2": menu_socios.listar_socios_interactivo,
        "3": menu_socios.editar_socio_interactivo,
        "4": menu_socios.eliminar_socio_interactivo,
    }

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción: ").strip()
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        
        if opcion == "5":
            print("¡Hasta luego!")
            break
        
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()