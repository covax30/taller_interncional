/**
 * pagos.js  —  apy/static/js/pagos.js
 * Maneja formsets dinámicos en Crear/Editar Pago.
 * Tres secciones independientes: Repuestos, Insumos, Herramientas.
 */

$(document).ready(function () {

    // ─────────────────────────────────────────────────────────
    // Contadores inyectados por el template en window.PagoConfig
    // ─────────────────────────────────────────────────────────
    var idx = {
        repuestos:    window.PagoConfig.indices.repuestos,
        insumos:      window.PagoConfig.indices.insumos,
        herramientas: window.PagoConfig.indices.herramientas
    };


    // ─────────────────────────────────────────────────────────
    // HELPER: agregar fila clonando un <template>
    // ─────────────────────────────────────────────────────────
    function agregarFila(templateId, contenedorId, prefix, clave) {
        var tmpl = document.getElementById(templateId);
        if (!tmpl) {
            console.error('Template no encontrado:', templateId);
            return;
        }

        // Clonamos el contenido del <template>
        var clone = document.importNode(tmpl.content, true);

        // Convertimos a string para reemplazar __prefix__
        var wrapper = document.createElement('div');
        wrapper.appendChild(clone);
        var html = wrapper.innerHTML;
        html = html.replace(/__prefix__/g, idx[clave]);

        // Insertamos la nueva fila en el contenedor
        var contenedor = document.getElementById(contenedorId);
        contenedor.insertAdjacentHTML('beforeend', html);

        // Actualizamos el TOTAL_FORMS del management_form de Django
        var totalInput = document.querySelector('[name="' + prefix + '-TOTAL_FORMS"]');
        if (totalInput) {
            idx[clave]++;
            totalInput.value = idx[clave];
        }

        recalcularTodo();
    }


    // ─────────────────────────────────────────────────────────
    // BOTONES AGREGAR
    // ─────────────────────────────────────────────────────────
    document.getElementById('add-repuesto').addEventListener('click', function () {
        agregarFila('repuesto-template', 'repuestos-formset', 'repuestos', 'repuestos');
    });

    document.getElementById('add-insumo').addEventListener('click', function () {
        agregarFila('insumo-template', 'insumos-formset', 'insumos', 'insumos');
    });

    document.getElementById('add-herramienta').addEventListener('click', function () {
        agregarFila('herramienta-template', 'herramientas-formset', 'herramientas', 'herramientas');
    });


    // ─────────────────────────────────────────────────────────
    // ELIMINAR FILA  (delegación en document)
    // ─────────────────────────────────────────────────────────
    $(document).on('click', '.remove-form', function () {
        var fila = $(this).closest('.repuesto-form, .insumo-form, .herramienta-form');
        var chk  = fila.find('input[type="checkbox"][name*="DELETE"]');

        if (chk.length) {
            // Fila guardada en BD → marcar DELETE y ocultar
            chk.prop('checked', true);
            fila.fadeOut(200);
        } else {
            // Fila nueva → eliminar del DOM
            fila.remove();
        }
        recalcularTodo();
    });


    // ─────────────────────────────────────────────────────────
    // CÁLCULO DE SUBTOTALES Y TOTALES
    // ─────────────────────────────────────────────────────────
    function subtotalFila(fila, selCant, selPrice, selSub) {
        var qty   = parseFloat(fila.find(selCant).val())  || 0;
        var price = parseFloat(fila.find(selPrice).val()) || 0;
        var sub   = qty * price;
        fila.find(selSub).val('$' + Math.round(sub).toLocaleString('es-CO'));
        return sub;
    }

    function totalSeccion(contenedorSel, claseForm, selCant, selPrice, selSub, idTotal) {
        var total = 0;
        $(contenedorSel + ' .' + claseForm).filter(':visible').each(function () {
            total += subtotalFila($(this), selCant, selPrice, selSub);
        });
        $('#' + idTotal).text('$' + Math.round(total).toLocaleString('es-CO'));
        return total;
    }

    function recalcularTodo() {
        var tRep = totalSeccion(
            '#repuestos-formset',    'repuesto-form',
            '.cantidad-repuesto',    '.precio-repuesto',
            '.subtotal-repuesto',    'total-repuestos'
        );
        var tIns = totalSeccion(
            '#insumos-formset',      'insumo-form',
            '.cantidad-insumo',      '.precio-insumo',
            '.subtotal-insumo',      'total-insumos'
        );
        var tHer = totalSeccion(
            '#herramientas-formset', 'herramienta-form',
            '.cantidad-herramienta', '.precio-herramienta',
            '.subtotal-herramienta', 'total-herramientas'
        );
        var gran = tRep + tIns + tHer;
        $('#gran-total-pago').text('$ ' + Math.round(gran).toLocaleString('es-CO'));
    }

    // Escuchar cambios en cantidad y precio de cualquier sección
    $(document).on('input change',
        '.cantidad-repuesto, .precio-repuesto,' +
        '.cantidad-insumo, .precio-insumo,' +
        '.cantidad-herramienta, .precio-herramienta',
        recalcularTodo
    );

    // Calcular al cargar (útil en edición con datos ya cargados)
    recalcularTodo();

});