/**
 * servicios.js - Manejo de formularios de servicios con Select2 y formsets
 * Versión: 2.0 - Con soporte completo para light/dark theme y select2 disabled
 */

// ============================================
// CONFIGURACIÓN GLOBAL DE SELECT2
// ============================================

$(document).ready(function() {
    
    // Inicializar todos los Select2 existentes
    initializeAllSelect2();
    
    // Re-inicializar Select2 cuando se abre un modal dinámico
    $(document).on('shown.bs.modal', '.modal', function() {
        $(this).find('select').select2({
            theme: 'bootstrap-5',
            width: '100%',
            dropdownParent: $(this),
            allowClear: true
        });
    });
});

/**
 * Inicializa todos los select2 en la página
 */
function initializeAllSelect2() {
    $('select.form-control, select.form-select, [data-select2="1"]').each(function() {
        if (!$(this).data('select2')) { // Evitar duplicar inicialización
            $(this).select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: $(this).attr('data-placeholder') || 'Seleccione una opción',
                allowClear: !$(this).prop('required'),
                dropdownParent: $(this).closest('.modal').length ? $(this).closest('.modal') : $(document.body),
                language: {
                    noResults: function() { return 'Sin resultados'; },
                    searching: function() { return 'Buscando...'; }
                }
            });
        }
    });
}

/**
 * Establece un valor en Select2 correctamente
 */
function setSelect2Value(selector, value, text = null) {
    const $select = $(selector);
    if (!$select.length) return false;
    
    // Si la opción no existe, crearla
    if (!$select.find(`option[value="${value}"]`).length && value && text) {
        $select.append(new Option(text, value, true, true));
    }
    
    $select.val(value).trigger('change');
    return true;
}

/**
 * Deshabilita un Select2 de forma visual y funcional
 */
function disableSelect2(selector) {
    const $select = $(selector);
    if (!$select.length) return;
    
    // Destruir Select2 anterior
    if ($select.data('select2')) {
        $select.select2('destroy');
    }
    
    // Deshabilitar select nativo
    $select.prop('disabled', true).addClass('disabled');
    
    // Re-inicializar con opciones de disabled
    $select.select2({
        theme: 'bootstrap-5',
        width: '100%',
        allowClear: false,
        minimumResultsForSearch: Infinity, // Quitar buscador
        dropdownParent: $(document.body),
        templateSelection: function(data) {
            return data.text; // Mostrar texto sin ícono de X
        }
    });
    
    // Bloquear visualmente el contenedor de Select2
    const $container = $select.next('.select2-container');
    $container.css({
        'opacity': '0.65',
        'pointer-events': 'none'
    }).addClass('select2-disabled-custom');
}

/**
 * Habilita un Select2
 */
function enableSelect2(selector) {
    const $select = $(selector);
    if (!$select.length) return;
    
    if ($select.data('select2')) {
        $select.select2('destroy');
    }
    
    $select.prop('disabled', false).removeClass('disabled');
    
    $select.select2({
        theme: 'bootstrap-5',
        width: '100%',
        allowClear: true,
        dropdownParent: $(document.body)
    });
    
    const $container = $select.next('.select2-container');
    $container.css({
        'opacity': '1',
        'pointer-events': 'auto'
    }).removeClass('select2-disabled-custom');
}

// ============================================
// AUTOSELECCIÓN Y DESHABILITAR CAMPOS
// ============================================

$(document).ready(function() {
    
    const perfilActualId = DjangoConfig?.perfil_actual_id || $('[data-perfil-actual]').data('perfil-actual');
    const empresaDefaultId = DjangoConfig?.empresa_default_id || $('[data-empresa-default]').data('empresa-default');
    
    // Esperar a que Select2 esté completamente inicializado
    setTimeout(function() {
        
        // Empresa
        if (empresaDefaultId && $('#id_empresa').length) {
            setSelect2Value('#id_empresa', empresaDefaultId);
            disableSelect2('#id_empresa');
        }
        
        // Empleado (Perfil actual)
        if (perfilActualId && $('#id_empleado').length) {
            setSelect2Value('#id_empleado', perfilActualId);
            disableSelect2('#id_empleado');
        }
        
    }, 500);
});

// ============================================
// AUTOCOMPLETAR DESDE ENTRADA
// ============================================

$(document).ready(function() {
    
    // Detectar si hay un parámetro ?entrada=id en la URL
    const params = new URLSearchParams(window.location.search);
    const entradaId = params.get('entrada');
    const entradaField = $('#id_id_entrada');
    
    if (entradaField.length) {
        // Si hay parámetro entrada en URL, cargar automáticamente
        if (entradaId) {
            setTimeout(function() {
                setSelect2Value('#id_id_entrada', entradaId);
                cargarDatosEntrada(entradaId);
            }, 300);
        }
        
        // Listener para cambios en el select de entrada
        entradaField.on('change', function() {
            const val = $(this).val();
            if (val) {
                cargarDatosEntrada(val);
            }
        });
    }
});

/**
 * Carga datos de una entrada via API
 */
function cargarDatosEntrada(entradaId) {
    if (!entradaId) return;
    
    const urlBase = "{% url 'apy:api_entrada_datos' 0 %}".replace('/0/', '/');
    
    fetch(urlBase + entradaId + '/')
        .then(res => res.json())
        .then(data => {
            if (!data.ok) {
                console.warn('[Entrada API] Error:', data);
                return;
            }
            
            console.info('[Entrada API] Datos cargados:', data);
            
            setTimeout(function() {
                // Vehículo
                if (data.vehiculo_id) {
                    setSelect2Value('#id_id_vehiculo', data.vehiculo_id, data.vehiculo_texto);
                }
                
                // Cliente
                if (data.cliente_id) {
                    setSelect2Value('#id_cliente', data.cliente_id, data.cliente_texto);
                }
            }, 100);
        })
        .catch(err => {
            console.warn('[Entrada API] Error fetch:', err);
        });
}

// ============================================
// FORMSETS: AGREGAR Y ELIMINAR FILAS
// ============================================

$(document).ready(function() {
    
    // Agregar Repuesto
    $('#add-repuesto').on('click', function(e) {
        e.preventDefault();
        agregarFilaFormset('repuestos', 'repuesto-template', '#repuestos-formset');
    });
    
    // Agregar Mantenimiento
    $('#add-mantenimiento').on('click', function(e) {
        e.preventDefault();
        agregarFilaFormset('mantenimientos', 'mantenimiento-template', '#mantenimientos-formset');
    });
    
    // Agregar Insumo
    $('#add-insumo').on('click', function(e) {
        e.preventDefault();
        agregarFilaFormset('insumos', 'insumo-template', '#insumos-formset');
    });
    
    // Eliminar filas
    $(document).on('click', '.remove-form', function(e) {
        e.preventDefault();
        $(this).closest('.repuesto-form, .mantenimiento-form, .insumo-form').remove();
        updateFormsetManagementForm();
        recalcularTotales();
    });
});

/**
 * Agrega una nueva fila al formset
 */
function agregarFilaFormset(formsetName, templateId, containerSelector) {
    const $container = $(containerSelector);
    const $template = $('#' + templateId);
    
    if (!$template.length) {
        console.error(`Template #${templateId} no encontrado`);
        return;
    }
    
    // Obtener el índice actual
    const $managementForm = $(`input[name="${formsetName}-TOTAL_FORMS"]`);
    const totalForms = parseInt($managementForm.val()) || 0;
    
    // Clonar el template y reemplazar __prefix__
    let html = $template.html();
    html = html.replace(/__prefix__/g, totalForms);
    
    // Añadir al contenedor
    $container.append(html);
    
    // Actualizar management form
    $managementForm.val(totalForms + 1);
    
    // Inicializar Select2 en los nuevos selects
    $container.find(`[name="${formsetName}-${totalForms}-id_repuesto"], [name="${formsetName}-${totalForms}-id_insumos"], [name="${formsetName}-${totalForms}-id_tipo_mantenimiento"]`).select2({
        theme: 'bootstrap-5',
        width: '100%',
        dropdownParent: $(document.body)
    });
    
    // Inicializar Select2 para el select de empleado (mantenimientos)
    $container.find(`[name="${formsetName}-${totalForms}-empleado"]`).select2({
        theme: 'bootstrap-5',
        width: '100%',
        dropdownParent: $(document.body)
    });
    
    console.log(`✓ Fila agregada a ${formsetName}`);
}

/**
 * Actualiza el management form de Django formset
 */
function updateFormsetManagementForm() {
    // Actualizar TOTAL_FORMS para repuestos
    const repuestosCount = $('#repuestos-formset .repuesto-form').length;
    $('input[name="repuestos-TOTAL_FORMS"]').val(repuestosCount);
    
    // Actualizar TOTAL_FORMS para mantenimientos
    const mantenimientosCount = $('#mantenimientos-formset .mantenimiento-form').length;
    $('input[name="mantenimientos-TOTAL_FORMS"]').val(mantenimientosCount);
    
    // Actualizar TOTAL_FORMS para insumos
    const insumosCount = $('#insumos-formset .insumo-form').length;
    $('input[name="insumos-TOTAL_FORMS"]').val(insumosCount);
}

// ============================================
// CÁLCULOS DE SUBTOTALES Y TOTALES
// ============================================

$(document).ready(function() {
    
    // Escuchar cambios en campos de cantidad y precio
    $(document).on('input change', '.cantidad-repuestos, .precio-repuestos, .cantidad-mantenimientos, .precio-mantenimientos, .cantidad-insumo, .precio-insumo', function() {
        recalcularTotales();
    });
});

/**
 * Recalcula todos los subtotales y totales
 */
function recalcularTotales() {
    
    // Repuestos
    let totalRepuestos = 0;
    $('#repuestos-formset .repuesto-form').each(function() {
        const cant = parseFloat($(this).find('.cantidad-repuestos').val()) || 0;
        const precio = parseFloat($(this).find('.precio-repuestos').val()) || 0;
        const subtotal = cant * precio;
        $(this).find('.subtotal-repuesto').val('$' + subtotal.toFixed(2));
        totalRepuestos += subtotal;
    });
    $('#total-repuestos').text('$' + totalRepuestos.toFixed(2));
    
    // Mantenimientos
    let totalMantenimientos = 0;
    $('#mantenimientos-formset .mantenimiento-form').each(function() {
        const cant = parseFloat($(this).find('.cantidad-mantenimientos').val()) || 0;
        const precio = parseFloat($(this).find('.precio-mantenimientos').val()) || 0;
        const subtotal = cant * precio;
        $(this).find('.subtotal-mantenimiento').val('$' + subtotal.toFixed(2));
        totalMantenimientos += subtotal;
    });
    $('#total-mantenimientos').text('$' + totalMantenimientos.toFixed(2));
    
    // Insumos
    let totalInsumos = 0;
    $('#insumos-formset .insumo-form').each(function() {
        const cant = parseFloat($(this).find('.cantidad-insumo').val()) || 0;
        const precio = parseFloat($(this).find('.precio-insumo').val()) || 0;
        const subtotal = cant * precio;
        $(this).find('.subtotal-insumos').val('$' + subtotal.toFixed(2));
        totalInsumos += subtotal;
    });
    $('#total-insumos').text('$' + totalInsumos.toFixed(2));
    
    // Gran total
    const granTotal = totalRepuestos + totalMantenimientos + totalInsumos;
    $('#gran-total-servicio').text('$' + granTotal.toFixed(2));
}

// ============================================
// MODALES DINÁMICOS
// ============================================

/**
 * Abre un modal y carga contenido via AJAX
 */
function abrirModalConFormulario(urlForm, modalSelector) {
    const $modal = $(modalSelector);
    
    if (!$modal.length) {
        console.error(`Modal ${modalSelector} no encontrado`);
        return;
    }
    
    $.ajax({
        url: urlForm,
        success: function(data) {
            $modal.find('.modal-body').html(data.html || data);
            
            // Re-inicializar Select2 dentro del modal
            setTimeout(function() {
                $modal.find('select').select2({
                    theme: 'bootstrap-5',
                    width: '100%',
                    dropdownParent: $modal
                });
            }, 100);
        },
        error: function(err) {
            console.error('Error cargando modal:', err);
            alert('Error al cargar el formulario. Intenta de nuevo.');
        }
    });
}

// ============================================
// LISTENERS PARA BOTONES DE MODALES
// ============================================

$(document).ready(function() {
    
    // Botón agregar vehículo
    $('[data-target="#modal-id_vehiculo"]').on('click', function() {
        abrirModalConFormulario(window.DjangoConfig?.urls?.id_vehiculo, '#modal-id_vehiculo');
    });
    
    // Botón agregar cliente
    $('[data-target="#modal-id_cliente"]').on('click', function() {
        abrirModalConFormulario(window.DjangoConfig?.urls?.cliente, '#modal-cliente');
    });
    
    // Etc para otros modales
});

// ============================================
// VALIDACIÓN ANTES DE GUARDAR
// ============================================

$(document).ready(function() {
    
    $('#servicio-form').on('submit', function(e) {
        
        // Validar que al menos haya un item (repuesto, mantenimiento o insumo)
        const totalItems = 
            $('#repuestos-formset .repuesto-form').length +
            $('#mantenimientos-formset .mantenimiento-form').length +
            $('#insumos-formset .insumo-form').length;
        
        if (totalItems === 0) {
            e.preventDefault();
            alert('Debes agregar al menos un repuesto, mantenimiento o insumo.');
            return false;
        }
        
        // Si todo está bien, permitir el submit
        return true;
    });
});

// ============================================
// INICIALIZACIÓN DE DATA CONFIG DE DJANGO
// ============================================

// Asegurar que window.DjangoConfig existe
if (typeof window.DjangoConfig === 'undefined') {
    window.DjangoConfig = {
        indices: { repuestos: 0, mantenimientos: 0, insumos: 0 },
        urls: {},
        perfil_actual_id: null,
        empresa_default_id: null
    };
}

console.log('✓ servicios.js cargado correctamente');