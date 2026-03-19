/**
 * servicios.js — Manejo de formsets, totales y modales AJAX
 */

// ══════════════════════════════════════════════════════
// HELPERS SELECT2
// ══════════════════════════════════════════════════════

function initSelect2En($ctx) {
    $ctx.find('select.form-control, select.form-select, select[data-select2]').each(function() {
        if (!$(this).data('select2')) {
            $(this).select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: $(this).attr('data-placeholder') || 'Seleccione una opción',
                allowClear: !$(this).prop('required'),
                dropdownParent: $(this).closest('.modal').length
                    ? $(this).closest('.modal')
                    : $(document.body),
                language: {
                    noResults: function() { return 'Sin resultados'; },
                    searching: function() { return 'Buscando...'; }
                }
            });
        }
    });
}

function setSelect2Value(selector, value, text) {
    var $sel = $(selector);
    if (!$sel.length || !value) return;
    if (!$sel.find('option[value="' + value + '"]').length && text) {
        $sel.append(new Option(text, value, true, true));
    }
    $sel.val(value).trigger('change');
}

function disableSelect2(selector) {
    var $sel = $(selector);
    if (!$sel.length) return;
    if ($sel.data('select2')) $sel.select2('destroy');
    $sel.prop('disabled', true);
    $sel.select2({
        theme: 'bootstrap-5',
        width: '100%',
        allowClear: false,
        minimumResultsForSearch: Infinity,
        dropdownParent: $(document.body)
    });
    $sel.next('.select2-container').css({ 'pointer-events': 'none', 'opacity': '0.75' });
}

// ══════════════════════════════════════════════════════
// INICIALIZACIÓN
// ══════════════════════════════════════════════════════

$(document).ready(function() {

    // Select2 en toda la página
    initSelect2En($(document.body));

    // Re-inicializar al abrir modales
    $(document).on('shown.bs.modal', '.modal', function() {
        initSelect2En($(this));
    });

    // ── Autoseleccionar Empresa y Empleado ──
    var perfilActualId   = "{{ perfil_actual_id|default:'' }}";
    var empresaDefaultId = "{{ empresa_default_id|default:'' }}";

    setTimeout(function() {
        if (empresaDefaultId && $('#id_empresa').length) {
            setSelect2Value('#id_empresa', empresaDefaultId);
            setTimeout(function() { disableSelect2('#id_empresa'); }, 100);
        }
        if (perfilActualId && $('#id_empleado').length) {
            setSelect2Value('#id_empleado', perfilActualId);
            setTimeout(function() { disableSelect2('#id_empleado'); }, 100);
        }
    }, 500);

    // ── Autocompletar desde entrada ──
    var params = new URLSearchParams(window.location.search);
    var entradaUrlId = params.get('entrada');
    if (entradaUrlId) {
        setTimeout(function() {
            setSelect2Value('#id_id_entrada', entradaUrlId);
            cargarDatosEntrada(entradaUrlId);
        }, 300);
    }

    $('#id_id_entrada').on('change', function() {
        var val = $(this).val();
        if (val) cargarDatosEntrada(val);
    });

    if ($('#id_id_entrada').val()) {
        $('#id_id_entrada').trigger('change');
    }
});

function cargarDatosEntrada(entradaId) {
    if (!entradaId) return;
    var url = window.DjangoConfig.urls.api_entrada_datos;
    if (!url) return;
    fetch(url.replace('/0/', '/' + entradaId + '/'))
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (!data.ok) return;
            setTimeout(function() {
                if (data.vehiculo_id) setSelect2Value('#id_id_vehiculo', data.vehiculo_id, data.vehiculo_texto);
                if (data.cliente_id)  setSelect2Value('#id_cliente',     data.cliente_id,  data.cliente_texto);
            }, 200);
        })
        .catch(function(err) { console.warn('[Entrada API]', err); });
}

// ══════════════════════════════════════════════════════
// MODALES AJAX — handler genérico para TODOS los botones
// ══════════════════════════════════════════════════════

// Mapa: data-target del botón → clave en DjangoConfig.urls
var MODAL_URL_MAP = {
    '#modal-id_vehiculo':           'id_vehiculo',
    '#modal-cliente':               'cliente',
    '#modal-id_cliente':            'cliente',
    '#modal-id_entrada':            'entrada',
    '#modal-id_salida':             'salida',
    '#modal-id_insumos':            'insumos',
    '#modal-id_repuesto':           'repuesto',
    '#modal-empleado':              'empleado',
    '#modal-id_tipo_mantenimiento': 'id_tipo_mantenimiento',
    '#modal-empresa':               'empresa'
};

$(document).on('click', '[data-toggle="modal"][data-target]', function(e) {
    e.preventDefault();
    e.stopPropagation();

    var target  = $(this).data('target');
    var $modal  = $(target);
    var urlKey  = MODAL_URL_MAP[target];
    var url     = urlKey && window.DjangoConfig && window.DjangoConfig.urls[urlKey];

    if (!$modal.length) {
        console.warn('[Modal] No se encontró:', target);
        return;
    }

    // Abrir el modal primero
    $modal.modal('show');

    if (!url) {
        console.warn('[Modal] No hay URL para:', target, '— urlKey:', urlKey);
        return;
    }

    // Mostrar spinner mientras carga
    $modal.find('.modal-body').html(
        '<div class="text-center p-4">' +
        '<div class="spinner-border text-primary"></div>' +
        '<p class="mt-2 text-muted small">Cargando...</p></div>'
    );

    $.ajax({
        url: url,
        type: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function(data) {
            var html = (data && data.html) ? data.html : data;
            $modal.find('.modal-body').html(html);

            // Inicializar Select2 dentro del modal
            setTimeout(function() {
                initSelect2En($modal);
            }, 100);
        },
        error: function(xhr) {
            $modal.find('.modal-body').html(
                '<div class="alert alert-danger">Error ' + xhr.status +
                ' al cargar el formulario.</div>'
            );
            console.error('[Modal AJAX] Error:', xhr.status, url);
        }
    });
});

// ══════════════════════════════════════════════════════
// FORMSETS — AGREGAR Y ELIMINAR FILAS
// ══════════════════════════════════════════════════════

$(document).ready(function() {

    $('#add-repuesto').on('click', function(e) {
        e.preventDefault();
        agregarFila('repuestos', 'repuesto-template', '#repuestos-formset');
    });

    $('#add-mantenimiento').on('click', function(e) {
        e.preventDefault();
        agregarFila('mantenimientos', 'mantenimiento-template', '#mantenimientos-formset');
    });

    $('#add-insumo').on('click', function(e) {
        e.preventDefault();
        agregarFila('insumos', 'insumo-template', '#insumos-formset');
    });

    $(document).on('click', '.remove-form', function(e) {
        e.preventDefault();
        var $fila = $(this).closest('.repuesto-form, .mantenimiento-form, .insumo-form');
        var prefijo = $fila.hasClass('repuesto-form')      ? 'repuestos'
                    : $fila.hasClass('mantenimiento-form') ? 'mantenimientos'
                    : 'insumos';
        $fila.remove();
        // Actualizar TOTAL_FORMS
        var count = $('#' + prefijo + '-formset .' + prefijo.slice(0,-1) + '-form').length;
        $('input[name="' + prefijo + '-TOTAL_FORMS"]').val(count);
        recalcularTotales();
    });
});

function agregarFila(formset, templateId, containerSelector) {
    var $container = $(containerSelector);
    var $template  = $('#' + templateId);
    var $total     = $('input[name="' + formset + '-TOTAL_FORMS"]');

    if (!$template.length) { console.error('Template no encontrado:', templateId); return; }

    var index = parseInt($total.val()) || 0;
    var html  = $template.html().replace(/__prefix__/g, index);

    $container.append(html);
    $total.val(index + 1);

    var $fila = $container.children().last();

    // Select2 solo en form-control (excluye form-select del mecánico)
    $fila.find('select.form-control').select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Seleccione una opción',
        allowClear: true,
        dropdownParent: $(document.body)
    });

    recalcularTotales();
}

// ══════════════════════════════════════════════════════
// TOTALES
// ══════════════════════════════════════════════════════

$(document).on('input change',
    '.cantidad-repuestos, .precio-repuestos, ' +
    '.cantidad-mantenimientos, .precio-mantenimientos, ' +
    '.cantidad-insumo, .precio-insumo',
    function() { recalcularTotales(); }
);

function recalcularTotales() {
    var totalRep = 0, totalMant = 0, totalIns = 0;

    $('#repuestos-formset .repuesto-form').each(function() {
        var c = parseFloat($(this).find('.cantidad-repuestos').val()) || 0;
        var p = parseFloat($(this).find('.precio-repuestos').val())   || 0;
        var s = c * p; totalRep += s;
        $(this).find('.subtotal-repuesto').val('$' + s.toLocaleString('es-CO'));
    });

    $('#mantenimientos-formset .mantenimiento-form').each(function() {
        var c = parseFloat($(this).find('.cantidad-mantenimientos').val()) || 0;
        var p = parseFloat($(this).find('.precio-mantenimientos').val())   || 0;
        var s = c * p; totalMant += s;
        $(this).find('.subtotal-mantenimiento').val('$' + s.toLocaleString('es-CO'));
    });

    $('#insumos-formset .insumo-form').each(function() {
        var c = parseFloat($(this).find('.cantidad-insumo').val()) || 0;
        var p = parseFloat($(this).find('.precio-insumo').val())   || 0;
        var s = c * p; totalIns += s;
        $(this).find('.subtotal-insumos').val('$' + s.toLocaleString('es-CO'));
    });

    $('#total-repuestos').text('$' + totalRep.toLocaleString('es-CO'));
    $('#total-mantenimientos').text('$' + totalMant.toLocaleString('es-CO'));
    $('#total-insumos').text('$' + totalIns.toLocaleString('es-CO'));
    $('#gran-total-servicio').text('$' + (totalRep + totalMant + totalIns).toLocaleString('es-CO'));
}

// Calcular al cargar
$(document).ready(function() {
    setTimeout(recalcularTotales, 400);
});

// ══════════════════════════════════════════════════════
// VALIDACIÓN AL GUARDAR
// ══════════════════════════════════════════════════════

$(document).ready(function() {
    $('#servicio-form').on('submit', function(e) {
        var total =
            $('#repuestos-formset .repuesto-form').length +
            $('#mantenimientos-formset .mantenimiento-form').length +
            $('#insumos-formset .insumo-form').length;
        if (total === 0) {
            e.preventDefault();
            alert('Debes agregar al menos un repuesto, mantenimiento o insumo.');
            return false;
        }
    });
});

console.log('✓ servicios.js cargado');