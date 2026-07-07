from services import gestor_socios, gestor_inscripciones, gestor_actividades
from ui.helpers import reactivar_socio_interactivo
from utils import validaciones_socios
from utils.inputs import input_choice, input_str, solicitar_dato

def mostrar_submenu():
    while True:
        print("\n" + "=" * 50)
        print("          GESTIÓN DE SOCIOS")
        print("=" * 50)
        print("1. Registrar nuevo socio")
        print("2. Listar socios")
        print("3. Editar datos de socio")
        print("4. Solicitar baja de socio")
        print("5. Solicitar reactivación de socio")
        print("6. Volver al menú principal")
        print("=" * 50)
        opcion = input_choice("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6"])
        if opcion == "1":
            registrar_socio()
        elif opcion == "2":
            listar_socios_submenu()
        elif opcion == "3":
            editar_socio()
        elif opcion == "4":
            baja_socio()
        elif opcion == "5":
            reactivar_socio()
        elif opcion == "6":
            break

def registrar_socio():
    print("\n--- NUEVO SOCIO ---")
    dni = solicitar_dato(
        "DNI (solo números, 7-8 dígitos): ", validaciones_socios.validar_dni, "DNI inválido."
    )
    socio_existente = gestor_socios.buscar_por_dni(dni)
    if socio_existente:
        if socio_existente.activo:
            print(f"Ya existe un socio activo con DNI {dni}.")
            return
        else:
            print(f"El DNI {dni} pertenece a un socio inactivo.")
            print("¿Desea reactivarlo o cancelar?")
            print("1. Reactivar")
            print("2. Cancelar")
            opcion = input_choice("Opción (1/2): ", ["1", "2"])
            if opcion == "1":
                reactivar_socio_interactivo(socio_existente)
            else:
                print("Operación cancelada.")
            return
    nombre = solicitar_dato(
        "Nombre completo: ", validaciones_socios.validar_nombre, "Nombre inválido."
    )
    telefono = solicitar_dato(
        "Teléfono: ", validaciones_socios.validar_telefono, "Teléfono inválido."
    )
    direccion = solicitar_dato("Dirección: ")
    email = solicitar_dato("Email: ", validaciones_socios.validar_email, "Email inválido.")
    print("Seleccione membresía:")
    print("1. Básica (hasta 3 actividades)")
    print("2. Premium (hasta 8 actividades)")
    opcion_memb = input_choice("Opción (1/2): ", ["1", "2"])
    membresia = "basica" if opcion_memb == "1" else "premium"
    mensaje = gestor_socios.alta_socio(dni, nombre, telefono, direccion, email, membresia)
    print(mensaje)

def listar_socios_submenu():
    while True:
        print("\n--- LISTAR SOCIOS ---")
        print("1. Todos los socios (activos e inactivos)")
        print("2. Socios morosos (período de gracia)")
        print("3. Socios activos")
        print("4. Socios inactivos")
        print("5. Ver detalle de un socio")
        print("6. Volver al menú anterior")
        opcion = input_choice("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6"])
        if opcion == "1":
            listar_todos()
        elif opcion == "2":
            listar_morosos()
        elif opcion == "3":
            listar_activos()
        elif opcion == "4":
            listar_inactivos()
        elif opcion == "5":
            ver_detalle_socio()
        elif opcion == "6":
            break

def _mostrar_lista(socios, titulo):
    if not socios:
        print("No hay socios que mostrar.")
        return
    print(f"\n--- {titulo} ---")
    for s in socios:
        estado = gestor_socios.obtener_estado(s)
        if estado == "activo":
            estado_texto = "AL DÍA"
        elif estado == "debe_cuota":
            estado_texto = "MOROSO"
        elif estado == "inactivo_por_deuda":
            estado_texto = "INACTIVO POR DEUDA"
        elif estado == "inactivo":
            estado_texto = "INACTIVO (BAJA MANUAL)"
        else:
            estado_texto = estado
        print(
            f"N°: {s.numero_socio} | DNI: {s.dni} | {s.nombre_completo} | Membresía: {s.membresia} | {estado_texto}"
        )

def listar_todos():
    socios = gestor_socios.listar_socios(mostrar_inactivos=True)
    _mostrar_lista(socios, "TODOS LOS SOCIOS")

def listar_activos():
    socios = gestor_socios.listar_socios_activos()
    _mostrar_lista(socios, "SOCIOS ACTIVOS")

def listar_inactivos():
    socios = gestor_socios.listar_socios_inactivos()
    _mostrar_lista(socios, "SOCIOS INACTIVOS")

def listar_morosos():
    socios = gestor_socios.listar_morosos()
    _mostrar_lista(socios, "SOCIOS MOROSOS (PERÍODO DE GRACIA)")

def ver_detalle_socio():
    identificador = input_str("Ingrese DNI o número de socio: ")
    socio = gestor_socios.obtener_detalle_socio(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    estado = gestor_socios.obtener_estado(socio)
    venc = gestor_socios.calcular_vencimiento(socio)
    print("\n--- DETALLE DEL SOCIO ---")
    print(f"Número de socio: {socio.numero_socio}")
    print(f"DNI: {socio.dni}")
    print(f"Nombre: {socio.nombre_completo}")
    print(f"Teléfono: {socio.telefono}")
    print(f"Dirección: {socio.direccion}")
    print(f"Email: {socio.email}")
    print(f"Membresía: {socio.membresia}")
    print(f"Fecha de inscripción: {socio.fecha_inscripcion.strftime('%d/%m/%Y')}")
    if socio.fin_cobertura:
        print(f"Último pago: {socio.fin_cobertura.strftime('%d/%m/%Y')}")
    print(f"Vencimiento actual: {venc.strftime('%d/%m/%Y')}")
    print(f"Estado: {estado}")
    if not socio.activo and socio.motivo_baja:
        print(f"Motivo de baja: {socio.motivo_baja}")
    if socio.fecha_cambio_membresia:
        print(f"Último cambio de membresía: {socio.fecha_cambio_membresia.strftime('%d/%m/%Y')}")
    inscripciones_activas = gestor_inscripciones.obtener_inscripciones_activas_vigentes(socio.numero_socio)
    if inscripciones_activas:
        print("\n--- INSCRIPCIONES ACTIVAS ---")
        for ins in inscripciones_activas:
            act = gestor_actividades.obtener_actividad(ins.id_actividad)
            nombre_act = act.nombre if act else "Desconocida"
            print(f"  • {nombre_act} - Turno: {ins.turno.capitalize()} (hasta {ins.fecha_fin.strftime('%d/%m/%Y')})")
    else:
        print("\nNo tiene inscripciones activas.")
    
def editar_socio():
    identificador = input_str("Ingrese DNI o número de socio a editar: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    if not socio.activo:
        print("Socio inactivo.")
        print("¿Desea reactivarlo o cancelar?")
        print("1. Reactivar")
        print("2. Cancelar")
        opcion = input_choice("Opción (1/2): ", ["1", "2"])
        if opcion == "1":
            if reactivar_socio_interactivo(socio):
                socio = gestor_socios.buscar_por_identificador(identificador)
                if socio.activo:
                    print("Socio reactivado. Ahora puede editar sus datos.")
                else:
                    print("La reactivación no se completó. No se puede editar.")
                    return
            else:
                print("Operación cancelada.")
                return
        else:
            print("Operación cancelada.")
            return
    print(f"Editando a {socio.nombre_completo} (deje vacío para no modificar)")
    nuevo_nombre = solicitar_dato(
        f"Nuevo nombre [{socio.nombre_completo}]: ",
        validaciones_socios.validar_nombre,
        "Nombre inválido.",
        permitir_vacio=True,
    )
    nuevo_telefono = solicitar_dato(
        f"Nuevo teléfono [{socio.telefono}]: ",
        validaciones_socios.validar_telefono,
        "Teléfono inválido.",
        permitir_vacio=True,
    )
    nueva_direccion = solicitar_dato(f"Nueva dirección [{socio.direccion}]: ", permitir_vacio=True)
    nuevo_email = solicitar_dato(
        f"Nuevo email [{socio.email}]: ",
        validaciones_socios.validar_email,
        "Email inválido.",
        permitir_vacio=True,
    )
    cambios = {}
    if nuevo_nombre:
        cambios["nombre_completo"] = nuevo_nombre
    if nuevo_telefono:
        cambios["telefono"] = nuevo_telefono
    if nueva_direccion:
        cambios["direccion"] = nueva_direccion
    if nuevo_email:
        cambios["email"] = nuevo_email
    if cambios:
        mensaje = gestor_socios.editar_socio(identificador, cambios)
        print(mensaje)
    else:
        print("No se realizaron cambios.")

def baja_socio():
    identificador = input_str("Ingrese DNI o número de socio a dar de baja: ")
    mensaje = gestor_socios.eliminar_socio_logico(identificador)
    print(mensaje)

def reactivar_socio():
    identificador = input_str("Ingrese DNI o número de socio a reactivar: ")
    socio = gestor_socios.buscar_por_identificador(identificador)
    if not socio:
        print("Socio no encontrado.")
        return
    reactivar_socio_interactivo(socio)