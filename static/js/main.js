document.addEventListener("DOMContentLoaded", function () {
  /* 1. Control del Menú Desplegable Móvil / Tablet */
  const menuBtn = document.getElementById("menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");
    });
  }

  /* 1.5. Control por Clic del Dropdown Catálogos en Header (Solución definitiva para evitar que se cierre) */
  const btnCatalogos = document.getElementById("btn-catalogos");
  const menuCatalogos = document.getElementById("menu-catalogos");
  const arrowCatalogos = document.getElementById("arrow-catalogos");
  const containerCatalogos = document.getElementById(
    "dropdown-catalogos-container",
  );

  if (btnCatalogos && menuCatalogos) {
    btnCatalogos.addEventListener("click", function (e) {
      e.stopPropagation();
      menuCatalogos.classList.toggle("hidden");
      if (arrowCatalogos) {
        arrowCatalogos.classList.toggle("rotate-180");
      }
    });

    // Cerrar al hacer clic fuera del desplegable
    document.addEventListener("click", function (e) {
      if (containerCatalogos && !containerCatalogos.contains(e.target)) {
        menuCatalogos.classList.add("hidden");
        if (arrowCatalogos) {
          arrowCatalogos.classList.remove("rotate-180");
        }
      }
    });
  }

  /* 2. Lógica del Formulario de Inscripciones (Crear / Editar) */
  const nroCedulaInput = document.getElementById("nro_cedula");
  const tipoCedulaSelect = document.getElementById("tipo_cedula");
  const idAlumnoInput = document.getElementById("id_alumno");
  const infoAlumnoDiv = document.getElementById("info_alumno");
  const errorAlumnoP = document.getElementById("error_alumno");
  const btnSubmit = document.getElementById("btn_submit");
  const selectOferta = document.getElementById("select_oferta");
  const infoOfertaDiv = document.getElementById("info_oferta");

  if (nroCedulaInput && selectOferta && btnSubmit) {
    function verificarHabilitarBoton() {
      if (idAlumnoInput && idAlumnoInput.value && selectOferta.value) {
        btnSubmit.disabled = false;
        btnSubmit.classList.remove("bg-indigo-300", "cursor-not-allowed");
        btnSubmit.classList.add(
          "bg-indigo-600",
          "hover:bg-indigo-700",
          "shadow-md",
        );
      }
    }

    // Función para actualizar y mostrar la información detallada de la oferta académica
    function actualizarInfoOferta() {
      const selectedOption = selectOferta.options[selectOferta.selectedIndex];
      if (selectedOption && selectedOption.value) {
        const tipoElem = document.getElementById("oferta_tipo");
        const precioElem = document.getElementById("oferta_precio");
        const cuotasElem = document.getElementById("oferta_cuotas");
        const montocuotaElem = document.getElementById("oferta_montocuota");

        if (tipoElem)
          tipoElem.textContent = selectedOption.getAttribute("data-tipo") || "";
        if (precioElem)
          precioElem.textContent =
            selectedOption.getAttribute("data-precio") || "";
        if (cuotasElem)
          cuotasElem.textContent =
            selectedOption.getAttribute("data-cuotas") || "";
        if (montocuotaElem)
          montocuotaElem.textContent =
            selectedOption.getAttribute("data-montocuota") || "";

        if (infoOfertaDiv) infoOfertaDiv.classList.remove("hidden");
      } else {
        if (infoOfertaDiv) infoOfertaDiv.classList.add("hidden");
      }
      verificarHabilitarBoton();
    }

    // Ejecutar inmediatamente al cargar la página (vital para modo edición)
    actualizarInfoOferta();

    // Evento al cambiar la opción del select de oferta manualmente
    selectOferta.addEventListener("change", actualizarInfoOferta);

    // Evento al buscar alumno presionando Enter en la cédula
    nroCedulaInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        const tipo = tipoCedulaSelect ? tipoCedulaSelect.value : "V";
        const nro = nroCedulaInput.value.trim();

        if (!nro) return;

        fetch(`/inscripciones/api/alumno?tipo=${tipo}&nro=${nro}`)
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              if (idAlumnoInput) idAlumnoInput.value = data.id;

              const nombreElem = document.getElementById("alumno_nombre");
              const correoElem = document.getElementById("alumno_correo");
              const whatsappElem = document.getElementById("alumno_whatsapp");
              const fotoElem = document.getElementById("alumno_foto");

              if (nombreElem)
                nombreElem.textContent = `${data.nombres} ${data.apellidos}`;
              if (correoElem) correoElem.textContent = data.correo;
              if (whatsappElem) whatsappElem.textContent = data.whatsapp;
              if (fotoElem)
                fotoElem.src = data.foto || "/static/uploads/default.png";

              if (infoAlumnoDiv) infoAlumnoDiv.classList.remove("hidden");
              if (errorAlumnoP) errorAlumnoP.classList.add("hidden");
              verificarHabilitarBoton();
            } else {
              if (idAlumnoInput) idAlumnoInput.value = "";
              if (infoAlumnoDiv) infoAlumnoDiv.classList.add("hidden");
              if (errorAlumnoP) errorAlumnoP.classList.remove("hidden");
              btnSubmit.disabled = true;
              btnSubmit.classList.add("bg-indigo-300", "cursor-not-allowed");
              btnSubmit.classList.remove(
                "bg-indigo-600",
                "hover:bg-indigo-700",
                "shadow-md",
              );
            }
          })
          .catch((err) => console.error("Error al buscar alumno:", err));
      }
    });
  }

  /* 3. Lógica del Formulario de Ofertas Académicas (Cálculo dinámico de cuotas) */
  const inputPrecio = document.getElementById("precio_en_divisas");
  const inputCuotas = document.getElementById("nro_partes_cuotas");
  const inputCadaCuota = document.getElementById("cada_una_de_en_divisas");
  const inputOcultoCuota = document.getElementById("input_oculto_cuota");

  function calcularCuotasOferta(forzar = false) {
    if (inputPrecio && inputCuotas && inputCadaCuota) {
      const precio = parseFloat(inputPrecio.value) || 0;
      const cuotas = parseInt(inputCuotas.value) || 1;

      if (cuotas > 0) {
        const valorCuota = (precio / cuotas).toFixed(2);
        // Solo recalcula automáticamente si se fuerza o si el campo de cuota está vacio/0.00
        if (
          forzar ||
          !inputCadaCuota.value ||
          inputCadaCuota.value === "0.00"
        ) {
          inputCadaCuota.value = valorCuota;
          if (inputOcultoCuota) inputOcultoCuota.value = valorCuota;
        }
      }
    }
  }

  if (inputPrecio && inputCuotas) {
    // Si al cargar los campos tienen valores pero el monto de cuota está vacío, calcularlo una vez
    calcularCuotasOferta(false);

    // Escuchar cambios al escribir manualmente en los inputs
    inputPrecio.addEventListener("input", () => calcularCuotasOferta(true));
    inputCuotas.addEventListener("input", () => calcularCuotasOferta(true));
  }

  /* 4. Lógica de Previsualización en Tiempo Real de Imágenes (Alumnos / Profesores) */
  function configurarPreviewImagen(inputId, previewId) {
    const inputFile = document.getElementById(inputId);
    const imagePreview = document.getElementById(previewId);

    if (inputFile && imagePreview) {
      inputFile.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove("hidden");
          };
          reader.readAsDataURL(file);
        }
      });
    }
  }

  // Activar previews para cédula y carnet (empleados tanto en alumnos como en profesores)
  configurarPreviewImagen("input_foto_cedula", "preview_cedula");
  configurarPreviewImagen("input_foto_carnet", "preview_carnet");
});
