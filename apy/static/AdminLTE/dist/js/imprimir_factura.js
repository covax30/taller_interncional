// Función para generar el PDF
async function generarPDF(id) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    try {
        // 1. Llamada a la URL que configuramos en urls.py
        const response = await fetch(`/apy/factura/json/${id}/`);
        if (!response.ok) throw new Error("No se encontró la factura");
        
        const data = await response.json();

        // --- DISEÑO DE LA FACTURA ---
        
        // Encabezado Empresa
        doc.setFontSize(16);
        doc.setTextColor(40);
        doc.text(data.empresa.nombre, 15, 20);
        
        doc.setFontSize(9);
        doc.text(`NIT: ${data.empresa.nit}`, 15, 26);
        doc.text(`Dirección: ${data.empresa.direccion}`, 15, 31);
        doc.text(`Tel: ${data.empresa.telefono}`, 15, 36);

        // Bloque Factura N°
        doc.setDrawColor(0);
        doc.setFillColor(240, 240, 240);
        doc.rect(145, 12, 50, 25, 'F');
        doc.setFont(undefined, 'bold');
        doc.text("FACTURA DE VENTA", 150, 20);
        doc.setFontSize(14);
        doc.text(`N° ${data.factura_nro}`, 150, 30);

        // Datos Cliente y Vehículo
        doc.setFontSize(10);
        doc.setFont(undefined, 'bold');
        doc.text("DATOS DEL CLIENTE", 15, 50);
        doc.setFont(undefined, 'normal');
        doc.text(`Nombre: ${data.cliente.nombre}`, 15, 56);
        doc.text(`C.C./NIT: ${data.cliente.documento}`, 15, 62);

        doc.setFont(undefined, 'bold');
        doc.text("DATOS DEL VEHÍCULO", 110, 50);
        doc.setFont(undefined, 'normal');
        doc.text(`Placa: ${data.vehiculo.placa}`, 110, 56);
        doc.text(`Vehículo: ${data.vehiculo.info}`, 110, 62);

        // --- TABLA DE SERVICIOS ---
        // Combinamos los items que vienen del JSON
        const rows = data.items.map(item => [
            item.cantidad,
            item.descripcion,
            `$${item.precio.toLocaleString('es-CO')}`,
            `$${item.subtotal.toLocaleString('es-CO')}`
        ]);

        doc.autoTable({
            startY: 70,
            head: [['Cant.', 'Descripción del Servicio / Repuesto', 'Precio Unit.', 'Subtotal']],
            body: rows,
            theme: 'grid',
            headStyles: { fillColor: [0, 51, 102] },
            styles: { fontSize: 8 }
        });

        // Totales
        let finalY = doc.lastAutoTable.finalY + 10;
        doc.setFontSize(12);
        doc.setFont(undefined, 'bold');
        doc.text(`TOTAL A PAGAR: $${data.subtotal_factura.toLocaleString('es-CO')}`, 130, finalY);

        // Descarga
        doc.save(`Factura_${data.factura_nro}_${data.vehiculo.placa}.pdf`);

    } catch (error) {
        console.error("Error:", error);
        alert("Error al obtener los datos de la factura: " + error.message);
    }
}

// Escuchador del botón 
document.addEventListener("click", function(e) {
    const btn = e.target.closest(".btn-pdf-factura");
    if (btn) {
        const id = btn.getAttribute("data-id");
        generarPDF(id);
    }
});