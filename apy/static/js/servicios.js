$(document).ready(function () {

    /* ═══════════════════════════════════════════════════════════════
       SELECT2
    ═══════════════════════════════════════════════════════════════ */
    function initSelect2($ctx) {
        $ctx.find('select.form-control').each(function () {
            if (!$(this).hasClass('select2-hidden-accessible')) {
                $(this).select2({
                    theme: 'bootstrap-5',
                    width: '100%',
                    placeholder: 'Seleccione una opción',
                    allowClear: true
                });
            }
        });
    }

    initSelect2($(document.body));
    $.fn.select2.defaults.set('selectionCssClass', ':all:');
    $(document).on('select2:open', function() {
        document.querySelector('.select2-search__field')?.removeAttribute('aria-hidden');
    });

    /* ═══════════════════════════════════════════════════════════════
       UTILIDADES
    ═══════════════════════════════════════════════════════════════ */
    function formatCOP(valor) {
        return '$' + Math.round(valor).toLocaleString('es-CO');
    }
    function limpiarMonto(texto) {
        return parseInt(String(texto || '').replace(/\D/g, '')) || 0;
    }

    /* ═══════════════════════════════════════════════════════════════
       TOTALES
    ═══════════════════════════════════════════════════════════════ */
    var SECCIONES = {
        repuestos:      { clase: '.repuesto-form',      idTotal: 'total-repuestos',      clsSub: '.subtotal-repuesto'      },
        mantenimientos: { clase: '.mantenimiento-form', idTotal: 'total-mantenimientos', clsSub: '.subtotal-mantenimiento' },
        insumos:        { clase: '.insumo-form',        idTotal: 'total-insumos',        clsSub: '.subtotal-insumos'       }
    };

    function recalcularSeccion(prefijo) {
        var cfg = SECCIONES[prefijo];
        if (!cfg) return;
        var total = 0;
        $(cfg.clase).each(function () {
            var cant   = parseFloat($(this).find('input[name*="cantidad"]').val())        || 0;
            var precio = parseFloat($(this).find('input[name*="precio_unitario"]').val()) || 0;
            var sub    = cant * precio;
            total += sub;
            $(this).find(cfg.clsSub).val(formatCOP(sub));
        });
        $('#' + cfg.idTotal).text(formatCOP(total));
        actualizarGranTotal();
    }

    function actualizarGranTotal() {
        var gran = 0;
        Object.values(SECCIONES).forEach(function (cfg) {
            gran += limpiarMonto($('#' + cfg.idTotal).text());
        });
        $('#gran-total-servicio').text(formatCOP(gran));
    }

    window.recalcular = recalcularSeccion;

    $(document).on('input change', 'input[name*="cantidad"], input[name*="precio_unitario"]', function () {
        var name = $(this).attr('name') || '';
        if      (name.startsWith('repuestos'))      recalcularSeccion('repuestos');
        else if (name.startsWith('mantenimientos')) recalcularSeccion('mantenimientos');
        else if (name.startsWith('insumos'))        recalcularSeccion('insumos');
    });

    setTimeout(function () { Object.keys(SECCIONES).forEach(recalcularSeccion); }, 300);

    /* ═══════════════════════════════════════════════════════════════
       ELIMINAR FILA
    ═══════════════════════════════════════════════════════════════ */
    $(document).on('click', '.remove-form', function () {
        var $fila = $(this).closest('.repuesto-form, .mantenimiento-form, .insumo-form');
        if (!$fila.length) return;
        var prefijo = $fila.hasClass('repuesto-form')      ? 'repuestos'
                    : $fila.hasClass('mantenimiento-form') ? 'mantenimientos'
                    : 'insumos';
        $fila.find('select.select2-hidden-accessible').each(function () {
            $(this).select2('destroy');
        });
        $fila.remove();
        recalcularSeccion(prefijo);
    });

    /* ═══════════════════════════════════════════════════════════════
       AGREGAR FILA
       CLAVE: el <template> de mantenimiento ya tiene las opciones
       de empleados renderizadas por Django → solo clonar + Select2
    ═══════════════════════════════════════════════════════════════ */
    window.addForm = function (type) {
        var container  = document.getElementById(type + '-formset');
        var template   = document.getElementById(type.slice(0, -1) + '-template');
        var totalForms = document.getElementById('id_' + type + '-TOTAL_FORMS');

        if (!container || !template || !totalForms) {
            console.error('[addForm] Elementos no encontrados para:', type);
            return;
        }

        var index = parseInt(totalForms.value);
        var html  = template.innerHTML.replace(/__prefix__/g, index);

        $(container).append(html);
        totalForms.value = index + 1;

        // initSelect2 aplica a select.form-control — que ahora incluye
        // el select del mecánico (cambiado de form-select a form-control)
        initSelect2($(container).children().last());
    };

    /* ═══════════════════════════════════════════════════════════════
       BOTONES AGREGAR
    ═══════════════════════════════════════════════════════════════ */
    $('#add-repuesto')     .on('click', function () { window.addForm('repuestos'); });
    $('#add-mantenimiento').on('click', function () { window.addForm('mantenimientos'); });
    $('#add-insumo')       .on('click', function () { window.addForm('insumos'); });

    /* ═══════════════════════════════════════════════════════════════
       MODALES AJAX
    ═══════════════════════════════════════════════════════════════ */
    $(document).on('click', '[data-toggle="modal"]', function () {
        var target = $(this).data('target');
        var urlKey = target.replace('#modal-', '').replace(/^id_/, '');
        var url    = window.DjangoConfig && window.DjangoConfig.urls[urlKey];
        if (!url) return;
        $.ajax({
            url: url,
            success: function (data) {
                var $modal = $(target);
                $modal.find('.modal-body').html(data.html || data);
                initSelect2($modal);
                $modal.modal('show');
            },
            error: function () { console.error('[Modal AJAX] Error:', url); }
        });
    });

});