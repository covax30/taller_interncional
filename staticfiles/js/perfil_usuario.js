// static/js/perfil_usuario.js
document.addEventListener('DOMContentLoaded', function () {
    const imageUploadForm = document.getElementById('image-upload-form') || document.querySelector('form[action*="actualizar_perfil_imagen"]');
    const userAvatarImg = document.getElementById('user-avatar-img');

    // Elementos del Formulario de Imagen INDEPENDIENTE
    const fileInputSolo = document.getElementById('id_profile_imagen_solo');
    let clearCheckboxSolo = document.getElementById('id_imagen_clear_solo');
    const btnGuardarImagenUnica = document.getElementById('btn-guardar-imagen-unica');

    // Elementos del Formulario PRINCIPAL
    const fileInputPrincipal = document.getElementById('id_profile_imagen');
    let clearCheckboxPrincipal = document.getElementById('id_imagen_clear');

    // UI
    const btnSeleccionar = document.getElementById('btn-seleccionar-archivo');
    const btnEliminar = document.getElementById('btn-eliminar-imagen');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (!userAvatarImg) return;
    const defaultAvatarUrl = userAvatarImg.src;

    function ensureClearCheckbox(id, form) {
        let el = document.getElementById(id);
        if (!el && form) {
            el = document.createElement('input');
            el.type = 'checkbox';
            el.id = id;
            el.name = 'imagen_clear';
            el.className = 'd-none';
            form.appendChild(el);
        }
        return el;
    }

    clearCheckboxSolo = ensureClearCheckbox('id_imagen_clear_solo', imageUploadForm);
    clearCheckboxPrincipal = ensureClearCheckbox('id_imagen_clear', document.querySelector('form[method="POST"][enctype="multipart/form-data"]'));

    // 1) Botón SELECCIONAR
    if (btnSeleccionar && fileInputSolo) {
        btnSeleccionar.addEventListener('click', () => fileInputSolo.click());
    }

    // 2) Cambio de archivo
    if (fileInputSolo && fileNameDisplay) {
        fileInputSolo.addEventListener('change', function (e) {
            if (e.target.files && e.target.files.length > 0) {
                const file = e.target.files[0];
                fileNameDisplay.textContent = 'Seleccionado: ' + file.name;
                if (btnGuardarImagenUnica) {
                    btnGuardarImagenUnica.disabled = false;
                    btnGuardarImagenUnica.classList.replace('btn-success', 'btn-primary');
                }
                const reader = new FileReader();
                reader.onload = (event) => userAvatarImg.src = event.target.result;
                reader.readAsDataURL(file);
                if (clearCheckboxSolo) clearCheckboxSolo.checked = false;
                if (clearCheckboxPrincipal) clearCheckboxPrincipal.checked = false;
                if (btnEliminar) btnEliminar.classList.replace('btn-danger', 'btn-outline-danger');
                if (fileInputPrincipal) fileInputPrincipal.files = this.files;
            }
        });
    }

    // 3) Botón ELIMINAR (CORREGIDO)
    if (btnEliminar) {
        btnEliminar.addEventListener('click', function (e) {
            e.preventDefault();
            if (!clearCheckboxSolo) return;

            // Preguntamos al usuario
            // perfil_usuario.js -> Dentro del evento btnEliminar
            if (confirm('¿Seguro que deseas eliminar tu imagen de perfil?')) {
                // 1. LIMPIEZA ABSOLUTA DE ARCHIVOS SELECCIONADOS
                if (fileInputSolo) fileInputSolo.value = ''; 
                if (fileInputPrincipal) fileInputPrincipal.value = '';

                // 2. MARCAR ELIMINACIÓN
                clearCheckboxSolo.checked = true;
                if (clearCheckboxPrincipal) clearCheckboxPrincipal.checked = true;

                // 3. ENVIAR
                if (imageUploadForm) imageUploadForm.submit();
            }
        });
    }
});