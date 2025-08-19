console.log("✅ notificaciones_stock.js cargado");
document.addEventListener('DOMContentLoaded', function() {
    // Configuración
    const API_URL = '/apy/api/repuestos-bajo-stock/'; 
    const POLLING_INTERVAL = 60000; // 1 minuto
    
    // Elementos del DOM
    const elements = {
        bellBtn: document.getElementById('btnNotificaciones'),
        badge: document.getElementById('stock-notification-badge'),
        count: document.getElementById('notification-count'),
        container: document.getElementById('stock-notifications-container')
    };
    
    // Función para actualizar la UI
    function updateUI(products = null, error = false) {
        if (error) {
            elements.container.innerHTML = `
                <a class="dropdown-item text-danger">
                    <i class="bi bi-exclamation-octagon me-2"></i>
                    Error cargando notificaciones
                </a>`;
            return;
        }
        
        if (!products || products.length === 0) {
            elements.badge.classList.add('d-none');
            elements.count.textContent = '0 Notificaciones';
            elements.container.innerHTML = `
                <a class="dropdown-item">
                    <i class="bi bi-check-circle me-2 text-success"></i>
                    Todo en orden
                </a>`;
            return;
        }
        
        // Mostrar notificaciones
        elements.badge.classList.remove('d-none');
        elements.badge.textContent = products.length;
        elements.count.textContent = `${products.length} Notificaciones`;
        
        elements.container.innerHTML = products.map(product => `
            <a class="dropdown-item" href="/admin/apy/repuesto/${product.id}/change/">
                <i class="bi bi-exclamation-triangle me-2 text-warning"></i>
                ${product.nombre}: ${product.stock} unidades (Mínimo: ${product.stock_minimo})
            </a>
        `).join('');
    }
    
    // Función para obtener datos del stock
    async function fetchStockData() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    }
    
    // Función principal para verificar stock
    async function checkStockLevels() {
        try {
            const products = await fetchStockData();
            updateUI(products);
        } catch (error) {
            updateUI(null, true);
        }
    }
    
    // Event Listeners
    elements.bellBtn.addEventListener('click', checkStockLevels);
    
    // Inicialización
    checkStockLevels(); // Carga inicial
    setInterval(checkStockLevels, POLLING_INTERVAL); // Actualización periódica
});