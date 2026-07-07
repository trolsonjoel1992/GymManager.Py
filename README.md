# Gestor de Gimnasio - Sistema de Administración

Sistema integral para la gestión de un gimnasio, desarrollado en Python con interfaz de consola. Permite administrar socios, actividades, inscripciones, asistencias, pagos y generar reportes estadísticos.

## Características principales

- **Gestión de socios**: alta, edición, baja lógica, reactivación con cálculo de deuda.
- **Membresías**: básica (hasta 2 actividades adicionales) y premium (hasta 4).
- **Control de morosidad**: período de gracia de 10 días, desactivación automática por falta de pago.
- **Actividades**: configurables con cupos por turno (mañana, tarde, noche).
- **Inscripciones**: límite según membresía, control de cupos, vigencia vinculada a la cobertura.
- **Asistencias**: marcación individual o masiva, cálculo de faltas mensuales y consecutivas.
- **Bajas automáticas por faltas**: se eliminan inscripciones cuando se superan 12 faltas al mes o 7 faltas consecutivas (excluye musculación).
- **Pagos**: registro, extensión de cobertura, cambio de membresía, historial.
- **Estadísticas**: concurrencia por actividad, asistencia por socio, estado de socios, ingresos mensuales.
- **Persistencia en JSON**: todos los datos se guardan en archivos `files/*.json`.

## Tecnologías

- Python 3.6+
- Librería estándar: `dataclasses`, `json`, `datetime`, `os`, `typing`
- `python-dateutil` para cálculos con meses

## Estructura del proyecto

```
.
├── domain/                        # Entidades (dataclasses)
│   ├── actividades.py
│   ├── asistencias.py
│   ├── inscripciones.py
│   ├── pagos.py
│   └── socios.py
├── persistence/                   # Repositorios para archivos JSON
│   ├── repositorio_actividades.py
│   ├── repositorio_asistencias.py
│   ├── repositorio_inscripciones.py
│   ├── repositorio_pagos.py
│   └── repositorio_socios.py
├── services/                      # Lógica de negocio (gestores)
│   ├── gestor_actividades.py
│   ├── gestor_asistencias.py
│   ├── gestor_estadisticas.py
│   ├── gestor_inscripciones.py
│   ├── gestor_pagos.py
│   └── gestor_socios.py
├── ui/                            # Menús de interfaz de usuario
│   ├── menu_actividades.py
│   ├── menu_asistencias.py
│   ├── menu_estadisticas.py
│   ├── menu_inscripciones.py
│   ├── menu_pagos.py
│   ├── menu_socios.py
│   └── helpers.py
├── utils/                         # Utilidades: validaciones e inputs
│   ├── inputs.py
│   └── validaciones_socios.py
├── files/                         # Archivos JSON de datos (se crean automáticamente)
├── main.py                        # Punto de entrada
└── README.md
```

## Instalación y ejecución

1. **Clonar el repositorio**:

   ```bash
   git clone <url-del-repositorio>
   cd gestor-gimnasio
   ```

2. **Instalar dependencias** (opcional, solo requiere `python-dateutil`):

   ```bash
   pip install python-dateutil
   ```

   Si no se instala, se puede reemplazar `relativedelta` con cálculos manuales, pero se recomienda tenerla.

3. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

   La primera ejecución creará la carpeta `files/` y los archivos JSON vacíos según sea necesario.

## Uso

Al iniciar, se muestra el menú principal con las siguientes opciones:

1. **Gestión de Socios** – alta, listado, edición, baja, reactivación.
2. **Gestión de Actividades** – consultar actividades predefinidas y su disponibilidad.
3. **Inscripciones** – inscribir/dar de baja socios en actividades.
4. **Control de Asistencia** – marcar asistencias, ver faltas, corregir asistencias del día.
5. **Registro de Pagos** – registrar pagos, cambiar membresía, ver estado de cuotas e historial.
6. **Estadísticas y Reportes** – concurrencia, asistencia, ingresos, etc.
7. **Salir** – finaliza la ejecución.

Cada submenú es autodescriptivo y solicita los datos necesarios con validación en tiempo real.

## Reglas de negocio relevantes

- **Membresía básica**: hasta 2 actividades adicionales (musculación es obligatoria e ilimitada).
- **Membresía premium**: hasta 4 actividades adicionales.
- **Cobertura**: la fecha de fin de cobertura se extiende con cada pago. Si no hay cobertura, no se permiten inscripciones.
- **Período de gracia**: 10 días después del vencimiento; el socio puede estar moroso pero activo.
- **Bajas por morosidad**: pasados los 10 días, el socio se desactiva automáticamente.
- **Faltas**: se cuentan por día (si hay al menos un presente, no se considera falta). Límites: 12 faltas en el mes o 7 consecutivas para que se dé de baja la inscripción (excepto musculación).
