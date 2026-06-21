from services import gestor_socios
from utils import validaciones_socios
from utils.inputs import solicitar_dato

def agregar_socio_interactivo():
    print("\n--- Nuevo Socio ---")
    dni = solicitar_dato("DNI (solo números, 7-8 dígitos): ", validaciones_socios.validar_dni, "DNI inválido.")
    nombre = solicitar_dato("Nombre completo: ", validaciones_socios.validar_nombre, "Nombre inválido.")
    telefono = solicitar_dato("Teléfono: ", validaciones_socios.validar_telefono, "Teléfono inválido.")
    direccion = solicitar_dato("Dirección: ")
    email = solicitar_dato("Email: ", validaciones_socios.validar_email, "Email inválido.")
    
    print("Seleccione membresía:")
    print("1. Básica (hasta 3 actividades)")
    print("2. Premium (hasta 8 actividades)")
    opcion_memb = solicitar_dato("Opción (1/2): ", lambda x: x in ("1","2"), "Opción inválida.")
    membresia = "basica" if opcion_memb == "1" else "premium"
    
    mensaje = gestor_socios.alta_socio(dni, nombre, telefono, direccion, email, membresia)
    print(mensaje)

def listar_socios_interactivo():
    socios = gestor_socios.listar_socios()
    if not socios:
        print("No hay socios activos.")
        return
    print("\n--- Socios Activos ---")
    for s in socios:
        estado_moroso = "MOROSO" if gestor_socios.es_moroso(s) else "AL DÍA"
        print(f"N°: {s.numero_socio} | DNI: {s.dni} | {s.nombre_completo} | Membresía: {s.membresia} | {estado_moroso}")

def editar_socio_interactivo():
    dni = input("DNI del socio a editar: ").strip()
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        print("Socio no encontrado.")
        return
    print(f"Editando a {socio.nombre_completo} (deje vacío para no modificar)")
    nuevo_nombre = solicitar_dato(f"Nuevo nombre [{socio.nombre_completo}]: ", validaciones_socios.validar_nombre, "Nombre inválido.", permitir_vacio=True)
    nuevo_telefono = solicitar_dato(f"Nuevo teléfono [{socio.telefono}]: ", validaciones_socios.validar_telefono, "Teléfono inválido.", permitir_vacio=True)
    nueva_direccion = solicitar_dato(f"Nueva dirección [{socio.direccion}]: ", permitir_vacio=True)
    nuevo_email = solicitar_dato(f"Nuevo email [{socio.email}]: ", validaciones_socios.validar_email, "Email inválido.", permitir_vacio=True)
    
    print("Nueva membresía (deje vacío para no cambiar):")
    print("1. Básica")
    print("2. Premium")
    opcion_memb = solicitar_dato("Opción (1/2) o Enter: ", lambda x: x in ("1","2",""), "Opción inválida.", permitir_vacio=True)
    nueva_membresia = None
    if opcion_memb == "1":
        nueva_membresia = "basica"
    elif opcion_memb == "2":
        nueva_membresia = "premium"
    
    cambios = {}
    if nuevo_nombre: cambios["nombre_completo"] = nuevo_nombre
    if nuevo_telefono: cambios["telefono"] = nuevo_telefono
    if nueva_direccion: cambios["direccion"] = nueva_direccion
    if nuevo_email: cambios["email"] = nuevo_email
    if nueva_membresia: cambios["membresia"] = nueva_membresia
    
    if cambios:
        mensaje = gestor_socios.editar_socio(dni, cambios)
        print(mensaje)
    else:
        print("No se realizaron cambios.")

def eliminar_socio_interactivo():
    dni = input("DNI del socio a eliminar (baja lógica): ").strip()
    mensaje = gestor_socios.eliminar_socio_logico(dni)
    print(mensaje)

def reactivar_socio_interactivo():
    identificador = input("Ingrese DNI o número de socio: ").strip()
    mensaje = gestor_socios.reactivar_socio(identificador)
    print(mensaje)

def ver_morosos():
    morosos = gestor_socios.listar_morosos()
    if not morosos:
        print("No hay socios morosos.")
        return
    print("\n--- Socios Morosos ---")
    for s in morosos:
        deuda = gestor_socios.cuotas_adeudadas(s)
        print(f"N°: {s.numero_socio} | DNI: {s.dni} | {s.nombre_completo} | Debe: {deuda} cuota(s)")

def mostrar_submenu():
    while True:
        print("\n--- GESTIÓN DE SOCIOS ---")
        print("1. Agregar socio")
        print("2. Listar socios activos")
        print("3. Editar socio")
        print("4. Eliminar socio (baja lógica)")
        print("5. Reactivar socio (inactivo)")
        print("6. Ver socios morosos")
        print("7. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            agregar_socio_interactivo()
        elif opcion == "2":
            listar_socios_interactivo()
        elif opcion == "3":
            editar_socio_interactivo()
        elif opcion == "4":
            eliminar_socio_interactivo()
        elif opcion == "5":
            reactivar_socio_interactivo()
        elif opcion == "6":
            ver_morosos()
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")