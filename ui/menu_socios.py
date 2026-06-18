from services import gestor_socios
from utils import validadores
from ui.inputs import solicitar_dato

def agregar_socio_interactivo():
    print("\n--- Nuevo Socio (complete todos los campos) ---")
    
    dni = solicitar_dato("DNI (solo números, 7-8 dígitos): ", validadores.validar_dni, "DNI inválido.")
    nombre = solicitar_dato("Nombre completo: ", validadores.validar_nombre, "Nombre inválido (no vacío y sin números).")
    telefono = solicitar_dato("Teléfono: ", validadores.validar_telefono, "Teléfono inválido (9-15 dígitos, opcional +).")
    direccion = solicitar_dato("Dirección: ")
    email = solicitar_dato("Email: ", validadores.validar_email, "Email inválido.")
    
    mensaje = gestor_socios.alta_socio(dni, nombre, telefono, direccion, email)
    print(mensaje)

def listar_socios_interactivo():
    socios = gestor_socios.listar_socios()
    if not socios:
        print("No hay socios activos.")
        return
        
    print("\n--- Socios Activos ---")
    for s in socios:
        print(f"ID: {s.id} | DNI: {s.dni} | {s.nombre_completo} | Tel: {s.telefono} | Email: {s.email} | Ingreso: {s.fecha_inscripcion}")

def editar_socio_interactivo():
    dni = input("DNI del socio a editar: ").strip()
    socio = gestor_socios.buscar_por_dni(dni)
    if not socio:
        print("Socio no encontrado.")
        return
    
    print(f"Editando a {socio.nombre_completo} (deje vacío para no modificar)")
    
    nuevo_nombre = solicitar_dato(f"Nuevo nombre [{socio.nombre_completo}]: ", validadores.validar_nombre, "Nombre inválido.", permitir_vacio=True)
    nuevo_telefono = solicitar_dato(f"Nuevo teléfono [{socio.telefono}]: ", validadores.validar_telefono, "Teléfono inválido.", permitir_vacio=True)
    nueva_direccion = solicitar_dato(f"Nueva dirección [{socio.direccion}]: ", permitir_vacio=True)
    nuevo_email = solicitar_dato(f"Nuevo email [{socio.email}]: ", validadores.validar_email, "Email inválido.", permitir_vacio=True)
    
    cambios = {}
    if nuevo_nombre: cambios["nombre_completo"] = nuevo_nombre
    if nuevo_telefono: cambios["telefono"] = nuevo_telefono
    if nueva_direccion: cambios["direccion"] = nueva_direccion
    if nuevo_email: cambios["email"] = nuevo_email
    
    if cambios:
        mensaje = gestor_socios.editar_socio(dni, cambios)
        print(mensaje)
    else:
        print("No se realizaron cambios.")

def eliminar_socio_interactivo():
    dni = input("DNI del socio a eliminar (baja lógica): ").strip()
    mensaje = gestor_socios.eliminar_socio_logico(dni)
    print(mensaje)