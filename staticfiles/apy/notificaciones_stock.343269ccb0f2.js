document.addEventListener('DOMContentLoaded', function () {
    const notificationBadge = document.getElementById('stock-notification-badge');
    const notificationCount = document.getElementById('notification-count');
    const notificationsContainer = document.getElementById('stock-notifications-container');

    // URL de la API que creaste en Django
    const API_URL = 'apy/apy/repuestos-bajo-stock/';

    function fetchNotifications() {
        fetch(API_URL)
            .then(response => response.json())
            .then(data => {
                const count = data.count;
                const notificaciones = data.notificaciones;

                // Actualiza el contador
                notificationCount.textContent = `${count} Notificaciones`;
                notificationBadge.textContent = count;

                // Muestra/oculta el badge
                if (count > 0) {
                    notificationBadge.classList.remove('d-none');
                } else {
                    notificationBadge.classList.add('d-none');
                }

                // Limpia y llena el contenedor de notificaciones
                notificationsContainer.innerHTML = '';
                if (notificaciones.length === 0) {
                    notificationsContainer.innerHTML = '<a href="#" class="dropdown-item">Sin notificaciones</a>';
                } else {
                    notificaciones.forEach(notificacion => {
                        const item = document.createElement('a');
                        item.href = '#'; // Puedes cambiar esto por la URL del detalle del repuesto
                        item.className = 'dropdown-item';
                        item.innerHTML = `<i class="bi bi-exclamation-triangle-fill text-warning me-2"></i> Stock bajo: ${notificacion.nombre}`;
                        notificationsContainer.appendChild(item);
                    });
                }
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }

    // Ejecuta la función al cargar la página
    fetchNotifications();

    // Actualiza las notificaciones cada 60 segundos (opcional)
    setInterval(fetchNotifications, 60000);
});