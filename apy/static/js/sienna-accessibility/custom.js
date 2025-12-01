document.addEventListener('DOMContentLoaded', function() {
    
    // Función que contiene toda la lógica de manipulación (traducción, eliminación y color de enlaces)
    const manipularMenu = (menu) => {
        
        // =======================================================
        // 1. TRADUCCIÓN DE ETIQUETAS
        // =======================================================
        const buttonLabels = {
            // Usamos tu lista para la traducción
            "Readable Font": "Fuente Legible",
            "Highlight Links": "Resaltar Enlaces",
            "Highlight Title": "Resaltar Título",
            "Monochrome": "Monocromo",
            "Low Saturation": "Baja Saturación",
            "High Saturation": "Alta Saturación",
            // Los contrastes Alto, Bajo y Oscuro ya no se traducen
            "Big Cursor": "Cursor Grande",
            "Stop Animations": "Detener Animaciones",
            "Reading Guide": "Guía de Lectura"
        };

        menu.querySelectorAll('.asw-btn').forEach(button => {
            const icon = button.querySelector('.material-icons');
            if (icon && icon.nextSibling) {
                const key = icon.nextSibling.nodeValue.trim();
                if (buttonLabels[key]) {
                    icon.nextSibling.nodeValue = ' ' + buttonLabels[key]; 
                }
            }
        });

        // =======================================================
        // 2. ELIMINACIÓN DE OPCIONES DE CONTRASTE
        // =======================================================
        const keysToRemove = [
            'low-contrast', 
            'high-contrast', 
            'dark-contrast'
        ];
        
        keysToRemove.forEach(function(key) {
            const button = menu.querySelector(`[data-key="${key}"]`);
            if (button) {
                button.remove();
            }
        });

        // =======================================================
        // 3. CORRECCIÓN DEL COLOR DEL ENLACE DE FOOTER (El problema actual)
        //    Forzamos el color con JS para anular el estilo #fff.
        // =======================================================
        const footerLink = menu.querySelector('.asw-footer a'); 
        if (footerLink) {
            // Forzamos el color de texto a claro (AdminLTE Dark)
            footerLink.style.color = '#c2c7d0'; 
        }
        
        console.log("Widget manipulado: Traducciones, eliminación y color de enlaces aplicados.");
    };

    // Primero, verifica si el menú ya está cargado (para cargas muy rápidas)
    const menuExistente = document.querySelector('.asw-menu');
    if (menuExistente) {
        manipularMenu(menuExistente);
        return; 
    }

    // Si el menú no existe, creamos el observador para esperar su inyección en el DOM
    const observador = new MutationObserver((mutationsList, observador) => {
        const menu = document.querySelector('.asw-menu');
        
        if (menu) {
            // ¡Elemento encontrado! Desconectamos el observador
            observador.disconnect();
            // Ejecutamos la lógica de manipulación
            manipularMenu(menu);
        }
    });

    // Empezar a observar el <body> para detectar la inyección del menú
    observador.observe(document.body, { childList: true, subtree: true });
});