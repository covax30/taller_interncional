// Gestión completa del modal unificado
class GestorServicioUnificado {
    constructor() {
        this.repuestos = [];
        this.insumos = [];
        this.mantenimientos = [];
        this.contadorId = 0;
        
        this.inicializarEventos();
        this.actualizarTotalesGlobales();
    }

    inicializarEventos() {
        // Eventos para repuestos
        $('#btn-agregar-repuesto').click(() => this.agregarRepuesto());
        $('#btn-agregar-insumo').click(() => this.agregarInsumo());
        $('#btn-agregar-mantenimiento').click(() => this.agregarMantenimiento());
        $('#btn-guardar-todo').click(() => this.guardarTodo());

        // Eventos para Enter
        $('#cantidad-repuesto, #precio-repuesto').keypress(e => {
            if (e.which === 13) this.agregarRepuesto();
        });
        
        $('#cantidad-insumo, #precio-insumo').keypress(e => {
            if (e.which === 13) this.agregarInsumo();
        });
        
        $('#cantidad-mantenimiento, #precio-mantenimiento, #descripcion-mantenimiento').keypress(e => {
            if (e.which === 13) this.agregarMantenimiento();
        });
    }

    // Métodos para repuestos
    agregarRepuesto() {
        const id = $('#select-repuesto').val();
        const nombre = $('#select-repuesto option:selected').text();
        const cantidad = parseInt($('#cantidad-repuesto').val());
        const precio = parseFloat($('#precio-repuesto').val());

        if (!this.validarDatos(id, cantidad, precio, 'repuesto')) return;

        const item = {
            id: this.contadorId++,
            id_repuesto: id,
            nombre: nombre,
            cantidad: cantidad,
            precio: precio,
            subtotal: cantidad * precio
        };

        this.repuestos.push(item);
        this.actualizarListaRepuestos();
        this.limpiarFormularioRepuesto();
        this.mostrarMensaje('Repuesto agregado correctamente', 'success');
    }

    // Métodos para insumos
    agregarInsumo() {
        const id = $('#select-insumo').val();
        const nombre = $('#select-insumo option:selected').text();
        const cantidad = parseInt($('#cantidad-insumo').val());
        const precio = parseFloat($('#precio-insumo').val());

        if (!this.validarDatos(id, cantidad, precio, 'insumo')) return;

        const item = {
            id: this.contadorId++,
            id_insumos: id,
            nombre: nombre,
            cantidad: cantidad,
            precio: precio,
            subtotal: cantidad * precio
        };

        this.insumos.push(item);
        this.actualizarListaInsumos();
        this.limpiarFormularioInsumo();
        this.mostrarMensaje('Insumo agregado correctamente', 'success');
    }

    // Métodos para mantenimientos
    agregarMantenimiento() {
        const id = $('#select-mantenimiento').val();
        const nombre = $('#select-mantenimiento option:selected').text();
        const cantidad = parseInt($('#cantidad-mantenimiento').val());
        const precio = parseFloat($('#precio-mantenimiento').val());
        const descripcion = $('#descripcion-mantenimiento').val();

        if (!this.validarDatos(id, cantidad, precio, 'mantenimiento')) return;

        const item = {
            id: this.contadorId++,
            id_tipo_mantenimiento: id,
            nombre: nombre,
            cantidad: cantidad,
            precio: precio,
            descripcion: descripcion,
            subtotal: cantidad * precio
        };

        this.mantenimientos.push(item);
        this.actualizarListaMantenimientos();
        this.limpiarFormularioMantenimiento();
        this.mostrarMensaje('Tipo de mantenimiento agregado correctamente', 'success');
    }

    // Validaciones
    validarDatos(id, cantidad, precio, tipo) {
        if (!id) {
            this.mostrarMensaje(`Seleccione un ${tipo}`, 'error');
            return false;
        }
        if (!cantidad || cantidad < 1) {
            this.mostrarMensaje('La cantidad debe ser mayor a 0', 'error');
            return false;
        }
        if (!precio || precio < 99) {
            this.mostrarMensaje('El precio debe ser mayor o igual a 99', 'error');
            return false;
        }
        return true;
    }

    // Actualización de listas (similar para los 3 tipos)
    actualizarListaRepuestos() {
        this.actualizarListaGenerica(this.repuestos, '#lista-repuestos', '#lista-vacia-repuestos', '#total-repuestos', 'repuesto');
    }

    actualizarListaInsumos() {
        this.actualizarListaGenerica(this.insumos, '#lista-insumos', '#lista-vacia-insumos', '#total-insumos', 'insumo');
    }

    actualizarListaMantenimientos() {
        this.actualizarListaGenerica(this.mantenimientos, '#lista-mantenimientos', '#lista-vacia-mantenimientos', '#total-mantenimientos', 'mantenimiento');
    }

    actualizarListaGenerica(lista, selectorTbody, selectorVacio, selectorTotal, tipo) {
        const tbody = $(selectorTbody);
        const vacio = $(selectorVacio);
        const totalSpan = $(selectorTotal);

        if (lista.length === 0) {
            tbody.hide();
            vacio.show();
            totalSpan.text('0.00');
        } else {
            vacio.hide();
            tbody.show().empty();
            
            let total = 0;
            lista.forEach(item => {
                total += item.subtotal;
                tbody.append(`
                    <tr data-id="${item.id}">
                        <td>${item.nombre}</td>
                        <td class="text-center">${item.cantidad}</td>
                        <td class="text-right">$${item.precio.toFixed(2)}</td>
                        <td class="text-right"><strong>$${item.subtotal.toFixed(2)}</strong></td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-outline-danger btn-eliminar" data-tipo="${tipo}" data-id="${item.id}">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `);
            });
            totalSpan.text(total.toFixed(2));
        }
        
        this.actualizarTotalesGlobales();
    }

    // Eliminación de items
    configurarEliminacion() {
        $(document).on('click', '.btn-eliminar', (e) => {
            const button = $(e.currentTarget);
            const tipo = button.data('tipo');
            const id = button.data('id');
            
            this.eliminarItem(tipo, id);
        });
    }

    eliminarItem(tipo, id) {
        switch(tipo) {
            case 'repuesto':
                this.repuestos = this.repuestos.filter(item => item.id !== id);
                this.actualizarListaRepuestos();
                break;
            case 'insumo':
                this.insumos = this.insumos.filter(item => item.id !== id);
                this.actualizarListaInsumos();
                break;
            case 'mantenimiento':
                this.mantenimientos = this.mantenimientos.filter(item => item.id !== id);
                this.actualizarListaMantenimientos();
                break;
        }
        this.mostrarMensaje('Item eliminado correctamente', 'info');
    }

    // Guardado completo
    async guardarTodo() {
        const totalItems = this.repuestos.length + this.insumos.length + this.mantenimientos.length;
        
        if (totalItems === 0) {
            this.mostrarMensaje('No hay items para guardar', 'error');
            return;
        }

        const $btn = $('#btn-guardar-todo');
        $btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Guardando...');

        try {
            // Guardar repuestos
            if (this.repuestos.length > 0) {
                await this.guardarPorTipo('repuestos', this.repuestos);
            }

            // Guardar insumos
            if (this.insumos.length > 0) {
                await this.guardarPorTipo('insumos', this.insumos);
            }

            // Guardar mantenimientos
            if (this.mantenimientos.length > 0) {
                await this.guardarPorTipo('mantenimientos', this.mantenimientos);
            }

            this.mostrarMensaje(`✅ Se guardaron ${totalItems} items correctamente`, 'success');
            
            // Limpiar todo después de guardar
            this.limpiarTodo();
            
            // Cerrar modal después de 2 segundos
            setTimeout(() => {
                $('#modal-unificado').modal('hide');
                location.reload();
            }, 2000);

        } catch (error) {
            this.mostrarMensaje('❌ Error al guardar: ' + error, 'error');
        } finally {
            $btn.prop('disabled', false).html('<i class="fas fa-save"></i> Guardar Todo');
        }
    }

    guardarPorTipo(tipo, datos) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: window.location.href,
                type: 'POST',
                data: {
                    [`${tipo}_multiples`]: JSON.stringify(datos),
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                success: (data) => {
                    if (data.success) {
                        resolve(data);
                    } else {
                        reject(data.message);
                    }
                },
                error: (xhr, status, error) => {
                    reject(error);
                }
            });
        });
    }

    // Utilidades
    limpiarFormularioRepuesto() {
        $('#cantidad-repuesto').val('1');
        $('#precio-repuesto').val('');
    }

    limpiarFormularioInsumo() {
        $('#cantidad-insumo').val('1');
        $('#precio-insumo').val('');
    }

    limpiarFormularioMantenimiento() {
        $('#cantidad-mantenimiento').val('1');
        $('#precio-mantenimiento').val('');
        $('#descripcion-mantenimiento').val('');
    }

    limpiarTodo() {
        this.repuestos = [];
        this.insumos = [];
        this.mantenimientos = [];
        this.actualizarListaRepuestos();
        this.actualizarListaInsumos();
        this.actualizarListaMantenimientos();
    }

    actualizarTotalesGlobales() {
        const totalRepuestos = this.repuestos.reduce((sum, item) => sum + item.subtotal, 0);
        const totalInsumos = this.insumos.reduce((sum, item) => sum + item.subtotal, 0);
        const totalMantenimientos = this.mantenimientos.reduce((sum, item) => sum + item.subtotal, 0);
        const totalGeneral = totalRepuestos + totalInsumos + totalMantenimientos;

        $('#total-global').text(totalGeneral.toFixed(2));
    }

    mostrarMensaje(mensaje, tipo) {
        const alertClass = tipo === 'error' ? 'alert-danger' : 
                          tipo === 'success' ? 'alert-success' : 'alert-info';
        
        $('#msg-global').html(`
            <div class="alert ${alertClass} alert-dismissible fade show">
                ${mensaje}
                <button type="button" class="close" data-dismiss="alert">&times;</button>
            </div>
        `);
    }
}

// Inicializar cuando el DOM esté listo
$(document).ready(function() {
    window.gestorServicio = new GestorServicioUnificado();
    window.gestorServicio.configurarEliminacion();
});