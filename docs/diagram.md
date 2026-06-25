flowchart TD
    A([Inicio]) --> B[Mostrar menú principal]
    B --> C{Opción seleccionada}
    
    C -->|1| D[Gestión de Socios]
    C -->|2| E[Gestión de Actividades]
    C -->|3| F[Gestión de Inscripciones]
    C -->|4| G[Control de Asistencias]
    C -->|5| H[Gestión de Pagos]
    C -->|6| I[Estadísticas y Reportes]
    C -->|7| J([Fin])

    %% ============================================
    %% 1. GESTIÓN DE SOCIOS (ACTUALIZADO)
    %% ============================================
    D --> D1[Mostrar submenú socios]
    D1 --> D2{Acción}
    
    %% 1.1 Registrar socio (nuevo flujo con reactivación)
    D2 -->|Registrar| D3[Ingresar datos + membresía]
    D3 --> D4{¿DNI existe?}
    D4 -->|No| D5[Crear nuevo socio]
    D5 --> D6[activo = True<br>fecha_ultimo_pago = hoy + 1 mes]
    D6 --> D7[Registrar pago automático<br>meses_cubiertos = 1]
    D7 --> D8[Guardar socio y pago]
    D8 --> D1
    
    D4 -->|Sí, activo| D9[Mensaje: ya existe activo]
    D9 --> D1
    
    D4 -->|Sí, inactivo| D10[Mostrar mensaje:<br>DNI pertenece a inactivo]
    D10 --> D11[Ofrecer reactivar o cancelar]
    D11 -->|Reactivar| D12[Ir a flujo de reactivación]
    D11 -->|Cancelar| D1
    D12 --> D1

    %% 1.2 Listar socios (submenú)
    D2 -->|Listar| D13[Mostrar submenú listar]
    D13 --> D14{Opción}
    D14 -->|Todos| D15[Mostrar todos los socios<br>activos e inactivos]
    D14 -->|Morosos| D16[Mostrar socios en período de gracia]
    D14 -->|Activos| D17[Mostrar socios activos]
    D14 -->|Inactivos| D18[Mostrar socios inactivos<br>con motivo de baja]
    D14 -->|Ver detalle| D19[Buscar por identificador<br>DNI o número]
    D15 --> D1
    D16 --> D1
    D17 --> D1
    D18 --> D1
    D19 --> D20{¿Existe?}
    D20 -->|Sí| D21[Mostrar todos los datos + estado]
    D20 -->|No| D22[Mensaje: no encontrado]
    D21 --> D1
    D22 --> D1

    %% 1.3 Editar socio (búsqueda por identificador)
    D2 -->|Editar| D23[Buscar por identificador<br>DNI o número]
    D23 --> D24{¿Existe?}
    D24 -->|Sí| D25[Modificar campos y membresía]
    D25 --> D26[Guardar cambios]
    D26 --> D1
    D24 -->|No| D27[Mensaje: no encontrado]
    D27 --> D1
    
    %% 1.4 Baja lógica (búsqueda por identificador)
    D2 -->|Baja| D28[Buscar por identificador<br>DNI o número]
    D28 --> D29{¿Existe y activo?}
    D29 -->|Sí| D30[Baja lógica:<br>activo = False<br>motivo_baja = 'manual']
    D30 --> D31[Guardar cambios]
    D31 --> D1
    D29 -->|No| D32[Mensaje: no encontrado o ya inactivo]
    D32 --> D1
    
    %% 1.5 Reactivar socio (búsqueda por identificador)
    D2 -->|Reactivar| D33[Buscar por identificador<br>DNI o número]
    D33 --> D34{¿Existe inactivo?}
    D34 -->|Sí| D35[Calcular meses a pagar]
    D35 --> D36[Mostrar información al usuario]
    D36 --> D37{Confirmar reactivación?}
    D37 -->|Sí| D38[Ejecutar reactivación]
    D38 --> D39[Registrar pago automático con<br>meses_cubiertos calculados]
    D39 --> D40[Actualizar socio:<br>activo = True<br>motivo_baja = None<br>fecha_ultimo_pago = hoy + 1 mes]
    D40 --> D41[Guardar socio y pago]
    D41 --> D1
    D37 -->|No| D42[Cancelar operación]
    D42 --> D1
    D34 -->|No| D43[Mensaje: no encontrado o ya activo]
    D43 --> D1
    
    D2 -->|Volver| B

    %% ============================================
    %% 5. GESTIÓN DE PAGOS (ACTUALIZADO)
    %% ============================================
    H --> H1[Mostrar submenú pagos]
    H1 --> H2{Acción}
    
    %% 5.1 Registrar pago (con verificación de inactivo)
    H2 -->|Registrar pago| H3[Buscar por identificador<br>DNI o número]
    H3 --> H4{¿Socio existe?}
    H4 -->|No| H5[Mensaje: socio no encontrado]
    H5 --> H1
    H4 -->|Sí| H6{¿Socio está activo?}
    H6 -->|No| H7[Ofrecer reactivar o cancelar]
    H7 -->|Reactivar| H8[Ejecutar flujo de reactivación<br>con pago automático]
    H8 --> H9[Finalizar: ya se registró pago]
    H9 --> H1
    H7 -->|Cancelar| H10[Cancelar registro]
    H10 --> H1
    H6 -->|Sí| H11[Ingresar monto y meses]
    H11 --> H12[Calcular nueva fecha de cobertura]
    H12 --> H13[Actualizar socio:<br>fecha_ultimo_pago = nueva_fecha]
    H13 --> H14[Registrar pago en historial]
    H14 --> H15[Mensaje de éxito]
    H15 --> H1
    
    %% 5.2 Ver estado de cuotas (búsqueda por identificador)
    H2 -->|Ver estado| H16[Buscar por identificador<br>DNI o número]
    H16 --> H17{¿Socio existe?}
    H17 -->|No| H18[Mensaje: socio no encontrado]
    H18 --> H1
    H17 -->|Sí| H19[Obtener estado del socio]
    H19 --> H20[Mostrar mensaje según estado:<br>AL DÍA / MOROSO / INACTIVO POR DEUDA / INACTIVO MANUAL]
    H20 --> H1
    
    %% 5.3 Ver historial de pagos (búsqueda por identificador)
    H2 -->|Ver historial| H21[Buscar por identificador<br>DNI o número]
    H21 --> H22{¿Socio existe?}
    H22 -->|No| H23[Mensaje: socio no encontrado]
    H23 --> H1
    H22 -->|Sí| H24[Obtener pagos del socio]
    H24 --> H25{¿Hay pagos?}
    H25 -->|No| H26[Mostrar: No hay pagos]
    H26 --> H1
    H25 -->|Sí| H27[Mostrar historial:<br>fecha, monto, meses cubiertos]
    H27 --> H1
    
    H2 -->|Volver| B

    %% ============================================
    %% PROCESOS EN BACKGROUND (SIN CAMBIOS)
    %% ============================================
    subgraph "Proceso de Reactivación"
        R1[Inicio reactivación] --> R2{¿motivo_baja?}
        R2 -->|manual| R3[Pagar 1 mes]
        R2 -->|mora| R4[Calcular fecha de baja:<br>fecha_ultimo_pago + 40 días]
        R4 --> R5[Obtener mes y año de la baja]
        R5 --> R6[Obtener mes y año actual]
        R6 --> R7{¿mismo mes y año?}
        R7 -->|Sí| R8[Pagar 1 mes<br>mes actual]
        R7 -->|No| R9[Pagar 2 meses<br>mes vencido + mes actual]
        R3 --> R10[Registrar pago:<br>meses_cubiertos = 1 o 2]
        R8 --> R10
        R9 --> R10
        R10 --> R11[Actualizar socio:<br>activo = True<br>motivo_baja = None<br>fecha_ultimo_pago = hoy + 1 mes]
        R11 --> R12[Fin reactivación]
    end
    
    subgraph "Proceso de Baja Automática"
        B1[Iniciar verificación] --> B2[Obtener todos los socios activos]
        B2 --> B3[Para cada socio]
        B3 --> B4{¿días_desde_vencimiento > 10?}
        B4 -->|Sí| B5[Desactivar socio:<br>activo = False<br>motivo_baja = 'mora']
        B5 --> B6[Guardar cambios]
        B6 --> B7[Fin del proceso]
        B4 -->|No| B7
    end