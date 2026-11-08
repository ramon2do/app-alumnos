# AppAlumnos — Sistema de Gestión Académica & Inscripciones

Plataforma web de gestión académica integral y arquitectura limpia (DDD / Onion Architecture) desarrollada con Python (Flask) y SQLite. Diseñada para administrar alumnos, profesores, ofertas académicas (cursos/diplomados), control de catálogos normalizados (horarios, duración, frecuencia), gestión de inscripciones con cálculo automático de cuotas y generación dinámica de reportes en PDF y Excel con imágenes.

## 🌐 Enlaces Oficiales y Despliegue

- **Sitio Web en Vivo (PythonAnywhere):** <https://ramon2do.pythonanywhere.com>
- **Repositorio Público en GitHub:** <https://github.com/ramon2do/app-alumnos>

## 🚀 Características Principales

- **Arquitectura Limpia & DDD (Domain-Driven Design):**
  - Separación estricta por capas: **Domain** (entidades, objetos de valor y repositorios), **Application** (casos de uso y DTOs), **Infrastructure** (base de datos SQLite, controladores Flask y servicios) y **Presentation** (plantillas Jinja2 y Tailwind CSS).
  - Inyección de dependencias centralizada mediante `container` de la infraestructura.
- **Diseño UI/UX Responsivo y Moderno:**
  - Interfaz fluida basada en **Tailwind CSS** con paleta en tonos slate e índigo, completamente adaptable a dispositivos móviles, tablets y escritorios.
  - Menú de navegación principal con menú desplegable (_dropdown_) para la gestión rápida de catálogos y contenedor adaptativo `w-full` en el header.
- **Gestión Completa de Alumnos y Profesores:**
  - Búsqueda dinámica vía **AJAX (fetch API)** por tipo y número de cédula al inscribir.
  - Subida y almacenamiento seguro de fotografías (`Foto_Cédula` y `Foto_Carnet`).
  - Integración con Value Objects para correo electrónico (`Correo`) y WhatsApp (`WhatsApp`).
  - **Preservación de Estado ante Errores:** Al ocurrir un error de validación o unicidad (ej. cédula o correo duplicado), los datos del formulario, las opciones seleccionadas y las imágenes subidas temporalmente **no se borran**, permitiendo al usuario corregir de inmediato.
- **Ofertas Académicas Dinámicas:**
  - Registro de Cursos, Talleres y Diplomados con precios en divisas, número de partes/cuotas y cálculo automático del monto individual por cuota.
- **Gestión de Inscripciones (Registro y Edición):**
  - Proceso interactivo con precarga instantánea de datos de alumno y detalles de oferta (precio, cuotas, tipo de programa).
  - Soporte completo para **Crear** y **Modificar/Editar** inscripciones existentes manteniendo la sincronía con los catálogos.
- **Generación Dinámica de Reportes:**
  - **PDF (ReportLab):** Reporte formal por oferta académica incluyendo fotografías de carnet de los alumnos inscritos y encabezados estilizados.
  - **Excel (OpenPyxl):** Exportación detallada de nóminas con fotos embebidas y formatos de celda.
  - Nombres de archivo generados dinámicamente según el nombre de la oferta académica (ej. `Inscritos_Diplomado_de_Python.pdf`).

## 📋 Credenciales de Acceso por Defecto

El sistema inicializa automáticamente una cuenta de administrador predeterminada la primera vez que se ejecuta la aplicación:

- **Correo:** `admin@appalumnos.com` _(configurable mediante `.env`)_
- **Contraseña:** `TuPasswordSeguro123` _(configurable mediante `.env`)_

> **Nota para Operadores Nuevos:** Si un nuevo operador o usuario administrativo requiere acceso al sistema, debe dirigirse a la vista de **Registro** en la plataforma para crear su cuenta previa al inicio de sesión.

## ⚙️ Configuración del Entorno (`.env`)

El proyecto utiliza un archivo de configuración de entorno para gestionar variables sensibles, credenciales de correo SMTP y pasarelas de mensajería (Whapi).

1. En la raíz del proyecto, localiza el archivo de ejemplo **`.env.example`**.
2. Duplica o renómbralo a **`.env`**:
   ```bash
   cp .env.example .env
   ```
3. Abre el archivo `.env` y configura tus propias credenciales y parámetros de integración:

   ```env
   SECRET_KEY=tu_clave_secreta_super_segura
   DATABASE_PATH=bdalumnos.db

   # Configuración de Servidor de Correo SMTP (para notificaciones a alumnos/profesores)
   SMTP_SERVER=smtp.tuservidor.com
   SMTP_PORT=587
   SMTP_USER=tu_correo@dominio.com
   SMTP_PASSWORD=tu_contraseña_smtp

   # Configuración de la API de WhatsApp (Whapi) para envío de mensajes automáticos
   WHAPI_TOKEN=tu_token_api_whapi_aqui
   WHAPI_ENDPOINT=https://gate.whapi.cloud/messages/text
   ```

## 📁 Estructura de Archivos

El proyecto mantiene una arquitectura en capas limpia y desacoplada:

```text
📦 AppAlumnos/
 ┣ 📁 application/
 ┃ ┣ 📁 dtos/                # Objetos de Transferencia de Datos
 ┃ ┗ 📁 use_cases/            # Casos de uso del negocio (CrearAlumnoUseCase, etc.)
 ┣ 📁 domain/
 ┃ ┗ 📁 academico/
 ┃   ┣ 📁 entities/           # Entidades (Alumno, Oferta, Inscripcion, etc.)
 ┃   ┣ 📁 value_objects/      # Objetos de valor (Correo, WhatsApp, Precio)
 ┃   ┗ 📁 repositories/         # Interfaces / Contratos de repositorios
 ┣ 📁 infrastructure/
 ┃ ┣ 📁 database/             # Conexión SQLite y scripts de esquema (schema.sql)
 ┃ ┣ 📁 repositories/         # Implementaciones SQLite de los repositorios
 ┃ ┣ 📁 web/                  # Blueprints / Controladores de Flask (alumnos, profesores, ofertas, inscripciones, auth)
 ┃ ┗ 📜 container.py          # Contenedor de inyección de dependencias
 ┣ 📁 static/
 ┃ ┣ 📁 css/                  # Hojas de estilo y Tailwind CSS
 ┃ ┣ 📁 js/                   # Javascript cliente defensivo (main.js)
 ┃ ┗ 📁 uploads/              # Almacenamiento de fotos de cédula y carnet
 ┣ 📁 templates/
 ┃ ┣ 📜 base.html             # Layout principal responsivo con Header y Dropdown
 ┃ ┣ 📁 alumnos/              # Vistas HTML de Alumnos (con manejo de form_data e imágenes temporales)
 ┃ ┣ 📁 profesores/           # Vistas HTML de Profesores
 ┃ ┣ 📁 ofertas/              # Vistas HTML de Ofertas Académicas
 ┃ ┣ 📁 inscripciones/        # Vistas HTML de Formularios y Listados de Inscripción
 ┃ ┗ 📁 auth/                 # Vistas HTML de autenticación y registro de operadores
 ┣ 📜 app.py                  # Punto de entrada de Flask y servidor WSGI
 ┣ 📜 .env                    # Variables de entorno locales (con credenciales SMTP y Whapi)
 ┣ 📜 .env.example            # Plantilla pública de variables de entorno
 ┣ 📜 bdalumnos.db            # Archivo de base de datos SQLite (generado automáticamente)
 ┗ 📜 README.md               # Documentación completa del proyecto
```

## 🗄️ Modelo Entidad-Relación (DER)

La base de datos relacional SQLite está totalmente normalizada y compuesta por las siguientes tablas principales:

1. **`tbl_alumnos`:** `Id` (PK), `Tipo_Cedula`, `Nro_Cedula` (UNIQUE), `Nombres`, `Apellidos`, `Genero`, `Fecha_Nacimiento`, `Correo` (UNIQUE), `WhatsApp`, `Foto_Cedula`, `Foto_Carnet`.
2. **`tbl_profesores`:** `Id` (PK), `Tipo_Cedula`, `Nro_Cedula` (UNIQUE), `Nombres`, `Apellidos`, `Area_Conocimiento`, `Genero`, `Fecha_Nacimiento`, `WhatsApp`, `Correo` (UNIQUE), `Foto_Cedula`, `Foto_Carnet`.
3. **`tbl_ofertas_academicas`:** `Id` (PK), `Oferta_Academica`, `Tipo`, `Precio_Divisas`, `Nro_Partes_Cuotas`, `Cada_Una_De_Divisas`.
4. **`tbl_horarios` / `tbl_duracion` / `tbl_frecuencia`:** Catálogos normalizados asociados a las inscripciones.
5. **`tbl_inscripciones`:** Relación clave foránea entre Alumno, Oferta, Profesor y Catálogos con fecha de inscripción.

## ⚙️ Instrucciones de Uso y Ejecución Local

1. Asegúrate de tener instalado **Python 3.10+** y `pip`.
2. Clona el repositorio e instala las dependencias del proyecto:
   ```bash
   pip install flask reportlab openpyxl pillow python-dotenv requests
   ```
3. Copia el archivo `.env.example` como `.env` y configura tus credenciales SMTP y de la API de Whapi:
   ```bash
   cp .env.example .env
   ```
4. Inicia la aplicación Flask ejecutando en la terminal:
   ```bash
   python app.py
   ```
   _(La aplicación iniciará automáticamente el servidor de desarrollo y sincronizará la base de datos `bdalumnos.db`)._
5. Abre tu navegador e ingresa a la dirección: **`http://127.0.0.1:5000`**.

## ☁️ Despliegue en PythonAnywhere

1. Subir los archivos del proyecto al directorio home en PythonAnywhere (ejemplo: `/home/tu_usuario/AppAlumnos`).
2. Configurar el entorno virtual e instalar dependencias.
3. Asegurarse de crear y configurar el archivo `.env` en la raíz del servidor con las credenciales reales de producción (SMTP y Whapi).
4. Configurar el archivo WSGI en la pestaña **Web** apuntando a `app.py`.
5. Presionar **Reload**.

---

## 🔄 Mecanismo de Replicación (Prompt Maestro Extendido y Detallado)

Si deseas replicar en su totalidad este sistema web utilizando una Inteligencia Artificial, utiliza el siguiente prompt exhaustivo:

```text
Actúa como un Desarrollador Web Full Stack Senior experto en Python, Arquitectura Limpia (Domain-Driven Design / Onion Architecture), Flask, Tailwind CSS y servicios de integración externa. Necesito que construyas desde cero una aplicación web completa denominada "AppAlumnos", diseñada para la gestión académica integral de una institución (alumnos, profesores, ofertas académicas, catálogos e inscripciones).

La aplicación debe estructurarse estrictamente bajo los principios de Arquitectura Limpia, separando responsabilidades en las siguientes capas físicas y lógicas dentro del repositorio:

1. CAPA DE DOMINIO (`domain/`):
   - Entidades de negocio puras (sin acoplamiento a frameworks web o bases de datos): Alumno, Profesor, OfertaAcademica e Inscripcion.
   - Objetos de Valor (Value Objects) para garantizar encapsulamiento e invariantes en campos críticos: Correo (validación de formato de email), WhatsApp (formato y prefijo telefónico) y Precio (gestión de divisas).
   - Interfaces / Contratos de Repositorios que definen los métodos de persistencia esperados (buscar por ID, listar, guardar, actualizar, eliminar, buscar por cédula).

2. CAPA DE APLICACIÓN (`application/`):
   - Casos de uso desacoplados (Use Cases) que implementan la lógica de negocio transaccional (ej. CrearAlumnoUseCase, CrearOfertaUseCase, CrearInscripcionUseCase, ListarInscripcionesUseCase, etc.).

3. CAPA DE INFRAESTRUCTURA (`infrastructure/`):
   - Base de Datos SQLite (`bdalumnos.db`) y scripts de inicialización de esquemas (`schema.sql`).
   - Implementaciones concretas de los repositorios utilizando consultas SQL nativas mediante sqlite3.
   - Contenedor de Inyección de Dependencias centralizado (`container.py`) que instancia los repositorios y casos de uso para que los controladores Flask accedan a ellos limpiamente.
   - Blueprints de Flask organizados como controladores web en `infrastructure/web/`:
     * alumnos.py (CRUD completo con subida de fotos de cédula y carnet, preservación de estado de formulario en caso de error, persistencia temporal de imágenes mediante inputs ocultos y mensajes limpios de validación de unicidad).
     * profesores.py (CRUD completo con los mismos patrones de resiliencia y subida de archivos).
     * ofertas.py (Gestión de Cursos, Talleres y Diplomados con cálculo automático del monto por cuota basado en el precio total y el número de partes).
     * inscripciones.py (Módulo de inscripción vinculado con búsqueda AJAX en tiempo real por cédula de alumno, precarga de datos y selección de oferta).
     * auth.py / rutas de registro (Módulo de autenticación y registro de operadores previos al inicio de sesión con validaciones de unicidad).
   - Servicios externos configurados mediante variables de entorno (cargadas con python-dotenv): integración SMTP para envío de correos electrónicos y servicio de mensajería API Whapi para notificaciones de WhatsApp basadas en los parámetros definidos en el archivo .env.

4. CAPA DE PRESENTACIÓN Y UX (`templates/` y `static/`):
   - Layout maestro (`base.html`) diseñado con Tailwind CSS (tonos slate e índigo), barra de navegación sticky de ancho completo (w-full) con menús desplegables (dropdowns) para la administración de catálogos (Horarios, Duración, Frecuencia).
   - Formularios inteligentes: todos los formularios deben implementar el patrón "preserve-state-on-error". Al fallar la validación por campos duplicados (como Cédula o Correo en restricciones UNIQUE de SQLite), el controlador intercepta el error técnico, lo traduce a un mensaje amigable tipo flash (`danger`), y re-renderiza la plantilla pasando `form_data=request.form` y los archivos temporales para evitar que se borren los datos introducidos o las imágenes seleccionadas.
   - Uso de inputs `type="date"` para selectores de fecha nativos y atributos `autocomplete="off"` en campos críticos para evitar interferencias de autocompletado del navegador.

5. REQUISITOS DE CONFIGURACIÓN Y ENTORNO:
   - Uso obligatorio de `.env.example` y generación de `.env` estructurado que contenga variables críticas como SECRET_KEY, DATABASE_PATH, credenciales completas de servidor SMTP (SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD) y parámetros de la pasarela de WhatsApp Whapi (WHAPI_TOKEN, WHAPI_ENDPOINT).
   - Compatibilidad total con entornos locales y de producción WSGI (como PythonAnywhere).
```

## 📞 Datos de Contacto y Soporte

- **Plataforma:** AppAlumnos — Sistema de Gestión Académica
- **Despliegue Web:** <https://ramon2do.pythonanywhere.com>
- **Código Fuente:** <https://github.com/ramon2do/app-alumnos>
