$(document).ready(function () {
    // ... (Mantén tu código de modales igual)

    // FUNCIÓN DE CÁLCULO MEJORADA
    window.recalcular = function(seccion) {
        let totalSeccion = 0;
        // Buscamos todas las filas de la sección
        const filas = document.querySelectorAll(`.${seccion}-form`);
        
        filas.forEach(row => {
            const inputCant = row.querySelector('input[name*="cantidad"]');
            const inputPrecio = row.querySelector('input[name*="precio_unitario"]');
            const inputSub = row.querySelector('input[class*="subtotal"]');

            const cant = parseFloat(inputCant?.value) || 0;
            const precio = parseFloat(inputPrecio?.value) || 0;
            const subtotal = cant * precio;
            
            totalSeccion += subtotal;

            if (inputSub) {
                inputSub.value = "$" + subtotal.toLocaleString('es-CO', { maximumFractionDigits: 0 });
            }
        });

        // Actualizar el total de la sección (Asegúrate que el ID sea total-insumos, etc)
        const labelTotal = document.getElementById(`total-${seccion}s`);
        if (labelTotal) {
            labelTotal.innerText = "$" + totalSeccion.toLocaleString('es-CO');
        }
        actualizarGranTotal();
    };

    function limpiarMonto(texto) {
        if (!texto) return 0;
        return parseInt(texto.replace(/\D/g, "")) || 0;
    }

    function actualizarGranTotal() {
        let granTotal = 0;
        ['insumos', 'repuestos', 'mantenimientos'].forEach(s => {
            const elem = document.getElementById(`total-${s}`);
            if (elem) granTotal += limpiarMonto(elem.innerText);
        });

        const granTotalElem = document.getElementById('gran-total-servicio');
        if (granTotalElem) {
            granTotalElem.innerText = "$" + granTotal.toLocaleString('es-CO');
        }
    }

    // EVENTO PARA DETECTAR CAMBIOS EN FILAS NUEVAS Y VIEJAS
    $(document).on('input', 'input[name*="cantidad"], input[name*="precio_unitario"]', function() {
        const name = $(this).attr('name');
        if (name.includes('insumos')) recalcular('insumo');
        if (name.includes('repuestos')) recalcular('repuesto');
        if (name.includes('mantenimientos')) recalcular('mantenimiento');
    });

    // BOTÓN ELIMINAR (Corregido para actualizar totales al borrar)
    $(document).on('click', '.remove-form', function () {
        const row = $(this).closest('.row');
        let seccion = '';
        if (row.hasClass('insumo-form')) seccion = 'insumo';
        else if (row.hasClass('repuesto-form')) seccion = 'repuesto';
        else if (row.hasClass('mantenimiento-form')) seccion = 'mantenimiento';
        
        row.remove();
        if (seccion) recalcular(seccion);
    });

    // --- EJECUCIÓN INICIAL ---
    // Esto calcula los valores apenas carga la página (importante tras el error de Guardar)
    setTimeout(() => {
        ['insumo', 'repuesto', 'mantenimiento'].forEach(s => recalcular(s));
    }, 500);
    // --- FUNCIÓN PARA AGREGAR NUEVAS FILAS (FORMSETS) ---
window.addForm = function (type) {
    // type recibe 'insumos', 'repuestos' o 'mantenimientos'
    const container = document.getElementById(`${type}-formset`);
    
    // El template siempre es en singular: 'insumo-template'
    const templateId = type.slice(0, -1) + "-template"; 
    const template = document.getElementById(templateId);
    
    // El contador de Django: 'id_insumos-TOTAL_FORMS'
    const totalForms = document.getElementById(`id_${type}-TOTAL_FORMS`);

    if (!container || !template || !totalForms) {
        console.error("Error: No se encontraron los elementos necesarios para agregar " + type);
        return;
    }

    // 1. Obtener el índice actual (cuántos hay ahora)
    let index = parseInt(totalForms.value);
    
    // 2. Tomar el HTML del template y reemplazar el prefijo por el número de índice
    let html = template.innerHTML.replace(/__prefix__/g, index);

    // 3. Insertar el nuevo HTML al final del contenedor
    container.insertAdjacentHTML('beforeend', html);
    
    // 4. Aumentar el contador para que Django sepa que hay una fila más
    totalForms.value = index + 1;
    
    console.log("Nueva fila añadida en " + type + " con índice: " + index);
};

// --- VINCULAR LOS BOTONES CON LA FUNCIÓN ---
$(document).ready(function() {
    document.getElementById('add-insumo')?.addEventListener('click', () => window.addForm('insumos'));
    document.getElementById('add-repuesto')?.addEventListener('click', () => window.addForm('repuestos'));
    document.getElementById('add-mantenimiento')?.addEventListener('click', () => window.addForm('mantenimientos'));
});
});