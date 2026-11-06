# AppAlumnos — Sistema de Gestión Académica & Inscripciones

Plataforma web de gestión académica integral y arquitectura limpia (DDD / Onion Architecture) desarrollada con Python (Flask) y SQLite. Diseñada para administrar alumnos, profesores, ofertas académicas (cursos/diplomados), control de catálogos normalizados (horarios, duración, frecuencia), gestión de inscripciones con cálculo automático de cuotas y generación dinámica de reportes en PDF y Excel con imágenes.

---

## 🌐 Enlaces Oficiales y Despliegue

* **Sitio Web en Vivo (PythonAnywhere):** [https://ramon2do.pythonanywhere.com](https://ramon2do.pythonanywhere.com)
* **Repositorio Público en GitHub:** [https://github.com/ramon2do/app-alumnos](https://github.com/ramon2do/app-alumnos)

---

## 🚀 Características Principales

* **Arquitectura Limpia & DDD (Domain-Driven Design):**
  * Separación estricta por capas: **Domain** (entidades, objetos de valor y repositorios), **Application** (casos de uso y DTOs), **Infrastructure** (base de datos SQLite, controladores Flask y servicios) y **Presentation** (plantillas Jinja2 y Tailwind CSS).
  * Inyección de dependencias centralizada mediante `container` de la infraestructura.
* **Diseño UI/UX Responsivo y Moderno:**
  * Interfaz fluida basada en **Tailwind CSS** con paleta en tonos slate e índigo, completamente adaptable a dispositivos móviles, tablets y escritorios.
  * Menú de navegación principal con menú desplegable (*dropdown*) para la gestión rápida de catálogos y contenedor adaptativo `w-full` en el header.
* **Gestión Completa de Alumnos:**
  * Búsqueda dinámica vía **AJAX (fetch API)** por tipo y número de cédula al inscribir.
  * Subida y almacenamiento de fotografías de carnet (`Foto_Carnet`).
  * Integración con Value Objects para correo electrónico (`Correo`) y WhatsApp (`WhatsApp`).
* **Ofertas Académicas Dinámicas:**
  * Registro de Cursos y Diplomados con precios en divisas, número de partes/cuotas y cálculo automático del monto individual por cuota.
* **Normalización de Catálogos Relacionales:**
  * Módulos CRUD completos e independientes para **Horarios**, **Duración** y **Frecuencia**, vinculados a través de llaves foráneas (`Id_Horario`, `Id_Duracion`, `Id_Frecuencia`).
* **Gestión de Inscripciones (Registro y Edición):**
  * Proceso interactivo con precarga instantánea de datos de alumno y detalles de oferta (precio, cuotas, tipo de programa).
  * Soporte completo para **Crear** y **Modificar/Editar** inscripciones existentes manteniendo la sincronía con los catálogos.
* **Generación Dinámica de Reportes:**
  * **PDF (ReportLab):** Reporte formal por oferta académica incluyendo fotografías de carnet de los alumnos inscritos y encabezados estilizados.
  * **Excel (OpenPyxl):** Exportación detallada de nóminas con fotos embebidas y formatos de celda.
  * Nombres de archivo generados dinámicamente según el nombre de la oferta académica (ej. `Inscritos_Diplomado_de_Python.pdf`).

---

## 📁 Estructura de Archivos

El proyecto mantiene una arquitectura en capas limpia y desacoplada:

```text
📦 AppAlumnos/
 ┣ 📁 application/
 ┃ ┣ 📁 dtos/                # Objetos de Transferencia de Datos (InscripcionDTO, etc.)
 ┃ ┗ 📁 use_cases/            # Casos de uso del negocio (CrearInscripcionUseCase, etc.)
 ┣ 📁 domain/
 ┃ ┗ 📁 academico/
 ┃   ┣ 📁 entities/           # Entidades (Alumno, Oferta, Inscripcion, etc.)
 ┃   ┣ 📁 value_objects/      # Objetos de valor (Correo, WhatsApp, Precio)
 ┃   ┗ 📁 repositories/         # Interfaces / Contratos de repositorios
 ┣ 📁 infrastructure/
 ┃ ┣ 📁 database/             # Conexión SQLite y scripts de esquema (schema.sql)
 ┃ ┣ 📁 repositories/         # Implementaciones SQLite de los repositorios
 ┃ ┣ 📁 web/                  # Blueprints / Controladores de Flask (alumnos, ofertas, inscripciones, reportes, catalogos)
 ┃ ┗ 📜 container.py          # Contenedor de inyección de dependencias
 ┣ 📁 static/
 ┃ ┣ 📁 css/                  # Hojas de estilo y Tailwind CSS
 ┃ ┣ 📁 js/                   # Javascript cliente defensivo (main.js)
 ┃ ┗ 📁 uploads/              # Almacenamiento de fotos de carnet de alumnos
 ┣ 📁 templates/
 ┃ ┣ 📜 base.html             # Layout principal responsivo con Header y Dropdown de Catálogos
 ┃ ┣ 📁 alumnos/              # Vistas HTML de Alumnos
 ┃ ┣ 📁 ofertas/              # Vistas HTML de Ofertas Académicas
 ┃ ┣ 📁 inscripciones/        # Vistas HTML de Formularios y Listados de Inscripción
 ┃ ┗ 📁 catalogos/            # Vistas HTML para Horarios, Duración y Frecuencia
 ┣ 📜 app.py                  # Punto de entrada de Flask y servidor WSGI
 ┣ 📜 bdalumnos.db            # Archivo de base de datos SQLite (generado automáticamente)
 ┗ 📜 README.md               # Documentación completa del proyecto
```

---

## 🗄️ Modelo Entidad-Relación (DER)

La base de datos relacional SQLite está totalmente normalizada y compuesta por las siguientes tablas principales:

1. **`tbl_alumnos`:** `Id` (PK), `Tipo_Cedula`, `Nro_Cedula` (UNIQUE), `Nombres`, `Apellidos`, `Correo`, `WhatsApp`, `Foto_Carnet`.
2. **`tbl_profesores`:** `Id` (PK), `Tipo_Cedula`, `Nro_Cedula` (UNIQUE), `Nombres`, `Apellidos`, `Area_Conocimiento`.
3. **`tbl_ofertas_academicas`:** `Id` (PK), `Oferta_Academica`, `Tipo`, `Precio_Divisas`, `Nro_Partes_Cuotas`, `Cada_Una_De_Divisas`.
4. **`tbl_horarios`:** `Id` (PK), `Horario`.
5. **`tbl_duracion`:** `Id` (PK), `Duracion`.
6. **`tbl_frecuencia`:** `Id` (PK), `Frecuencia`.
7. **`tbl_inscripciones`:**
   * `Id` (INTEGER, PK, Autoincremental)
   * `Id_Alumno` (INTEGER, FK a `tbl_alumnos.Id`)
   * `Id_Oferta` (INTEGER, FK a `tbl_ofertas_academicas.Id`)
   * `Id_Profesor` (INTEGER, FK a `tbl_profesores.Id`)
   * `Id_Horario` (INTEGER, FK a `tbl_horarios.Id`)
   * `Id_Duracion` (INTEGER, FK a `tbl_duracion.Id`)
   * `Id_Frecuencia` (INTEGER, FK a `tbl_frecuencia.Id`)
   * `Fecha_Inscripcion` (TEXT / TIMESTAMP)

---

## ⚙️ Instrucciones de Uso y Ejecución Local

1. Asegúrate de tener instalado **Python 3.10+** y `pip`.
2. Clona el repositorio e instala las dependencias del proyecto:
   ```bash
   pip install flask reportlab openpyxl pillow
   ```
3. Verifica la estructura del proyecto y asegúrate de contar con el directorio `static/uploads/`.
4. Inicia la aplicación Flask ejecutando en la terminal:
   ```bash
   python app.py
   ```
   *(La aplicación iniciará automáticamente el servidor de desarrollo y creará/sincronizará el archivo de base de datos `bdalumnos.db`).*
5. Abre tu navegador e ingresa a la dirección: **`http://127.0.0.1:5000`**.

---

## ☁️ Despliegue en PythonAnywhere

1. Subir los archivos del proyecto al directorio home en PythonAnywhere (ejemplo: `/home/tu_usuario/AppAlumnos`).
2. Configurar el entorno virtual con Flask, ReportLab y OpenPyxl.
3. En la pestaña **Web**, abre el archivo de configuración WSGI (`/var/www/tu_usuario_pythonanywhere_com_wsgi.py`) y agrega el punto de entrada:
   ```python
   import sys
   import os

   project_home = '/home/tu_usuario/AppAlumnos'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```
4. Presiona **Reload** en la pestaña Web de PythonAnywhere.

---

## 🔄 Mecanismo de Replicación (Prompt Maestro 100%)

Si deseas replicar en su totalidad este sistema web utilizando una Inteligencia Artificial, utiliza el siguiente prompt detallado:

```text
Actúa como un Desarrollador Web Full Stack Senior experto en Python (Flask), Arquitectura Limpia (DDD / Domain-Driven Design) y Tailwind CSS. Necesito que crees desde cero un sistema de gestión académica integral denominado "AppAlumnos".

El sistema debe estar estructurado en capas desacopladas: domain (entities, value_objects, repositories), application (dtos, use_cases), infrastructure (database, repositories, web/blueprints, container) y templates/static.

### Requerimientos Técnicos y Funcionales detallados:

1. Arquitectura y Dominio:
   - Implementar entidades de Alumno, OfertaAcademica, Profesor, Inscripcion, Horario, Duracion y Frecuencia.
   - Utilizar Value Objects para validación de Correo, WhatsApp y Precio.
   - Usar un contenedor de dependencias (container.py) para inyectar repositorios de SQLite en los blueprints de Flask.

2. Base de Datos SQLite (bdalumnos.db):
   - Crear esquemas normalizados con llaves foráneas para inscripciones: Id_Alumno, Id_Oferta, Id_Profesor, Id_Horario, Id_Duracion e Id_Frecuencia.
   - Tablas independientes para los catálogos tbl_horarios, tbl_duracion y tbl_frecuencia.

3. Interfaz de Usuario y UX (Tailwind CSS & JavaScript):
   - Layout base responsivo (base.html) con un Header sticky de ancho completo (w-full), adaptabilidad completa para tablets y menú desplegable (dropdown) "Catálogos" para acceder a Horarios, Duración y Frecuencia.
   - Javascript cliente defensivo (main.js) para búsqueda AJAX de alumnos por cédula al presionar Enter, mostrando foto de carnet y datos de contacto.
   - Formulario de inscripción compatible tanto para Crear como para Editar, con actualización instantánea de información de cuotas y precios de la oferta seleccionada.

4. Exportación y Reportes:
   - Rutas para descargar reportes en PDF (con ReportLab) y Excel (con OpenPyxl) filtrados por oferta académica.
   - Incluir las fotografías de los alumnos embebidas en las celdas/filas.
   - Generar el nombre de archivo descargable concatenando el nombre formateado de la Oferta Académica (ejemplo: Inscritos_Diplomado_de_Python.pdf).
```

---

## 📞 Datos de Contacto y Soporte

* **Plataforma:** AppAlumnos — Sistema de Gestión Académica
* **Despliegue Web:** [https://ramon2do.pythonanywhere.com](https://ramon2do.pythonanywhere.com)
* **Código Fuente:** [https://github.com/ramon2do/app-alumnos](https://github.com/ramon2do/app-alumnos)