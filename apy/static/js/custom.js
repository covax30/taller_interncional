document.addEventListener('DOMContentLoaded', function() {
    const logoutForm = document.getElementById('logout-form');

    if (logoutForm) {
        logoutForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Detectamos el tema actual del sistema para que la alerta responda
            const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';

            Swal.fire({
                title: '¿Cerrar sesión?',
                text: "Estás a punto de salir del sistema.",
                icon: 'warning',
                showCancelButton: true,
                // Colores estándar que contrastan bien en ambos modos
                confirmButtonColor: '#d33', 
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, salir',
                cancelButtonText: 'Cancelar',
                // Dejamos que el fondo y color de texto sean fluidos
                background: isDark ? '#343a40' : '#ffffff',
                color: isDark ? '#ffffff' : '#212529',
            }).then((result) => {
                if (result.isConfirmed) {
                    logoutForm.submit();
                }
            });
        });
    }
});