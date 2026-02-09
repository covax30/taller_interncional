
function cargarImagen(url) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        img.src = url;
        img.onload = () => resolve(img);
        img.onerror = (e) => reject(new Error("No se pudo cargar el logo en: " + url));
    });
}

async function generarPDF(id) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    try {
        // --- CARGAR LOGO Y DATOS EN PARALELO ---
        const logoUrl = "/static/AdminLTE/dist/img/logo_taller.png";
        const [imgLogo, response] = await Promise.all([
            cargarImagen(logoUrl),
            fetch(`/apy/factura/json/${id}/`)
        ]);

        if (!response.ok) throw new Error("No se encontró la factura");
        const data = await response.json();

        // --- DISEÑO DEL ENCABEZADO ---
        doc.addImage(imgLogo, 'PNG', 15, 12, 25, 25);

        doc.setFontSize(16);
        doc.setFont("times", "italic");
        doc.setTextColor(40);
        doc.text(data.empresa.nombre, 45, 20);

        doc.setFontSize(12);
        doc.setTextColor(100);
        doc.text(`NIT: ${data.empresa.nit}`, 100, 26, { align: "center" });
        doc.text(`Dirección: ${data.empresa.direccion}`, 100, 31, { align: "center" });
        doc.text(`Tel: ${data.empresa.telefono}`, 100, 36, { align: "center" });

        // Bloque N° Factura (se mantiene igual a la derecha)
        doc.setFillColor(240, 240, 240);
        doc.rect(145, 25, 35, 15, 'F');
        doc.setFont("courier", 'bold');
        doc.setTextColor(0);
        doc.setFontSize(9);
        doc.text("FACTURA DE VENTA", 147, 30);
        doc.setFontSize(10);
        doc.text(`N° ${data.factura_nro}`, 162, 35, { align: "center" });

        // --- SECCIÓN: DATOS DEL CLIENTE Y VEHÍCULO (DISEÑO VERTICAL) ---
        let yPos = 40;
        const anchoTotal = 180;
        const xInicio = 15;

        // Configuración de colores
        const azulClaroFondo = [255, 255, 255];
        const azulBorde = [0, 51, 102];
        const azulEtiqueta = [0, 51, 102];

        doc.setFontSize(9);
        doc.setDrawColor(...azulBorde);

        // --- BLOQUE CLIENTE ---
        // Fila 1: Nombre
        doc.setFillColor(...azulClaroFondo);
        doc.roundedRect(xInicio, yPos, anchoTotal, 7, 1, 1, 'FD');
        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("CLIENTE:", xInicio + 3, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.cliente.nombre}`, xInicio + 25, yPos + 5.5);

        // Fila 2: NIT y Teléfono
        yPos += 9;
        doc.setFillColor(...azulClaroFondo);
        doc.roundedRect(xInicio, yPos, anchoTotal, 7, 1, 1, 'FD');
        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("NIT/C.C.:", xInicio + 3, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.cliente.documento}`, xInicio + 25, yPos + 5.5);

        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("TELÉFONO:", xInicio + 100, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.cliente.telefono}`, xInicio + 125, yPos + 5.5);

        // Fila 3: Dirección
        yPos += 9;
        doc.setFillColor(...azulClaroFondo);
        doc.roundedRect(xInicio, yPos, anchoTotal, 7, 1, 1, 'FD');
        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("DIRECCIÓN:", xInicio + 3, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.cliente.direccion}`, xInicio + 25, yPos + 5.5);

        // --- BLOQUE VEHÍCULO ---
        yPos += 11; // Espacio de separación entre secciones
        doc.setFillColor(...azulClaroFondo);
        doc.roundedRect(xInicio, yPos, anchoTotal, 7, 1, 1, 'FD');
        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("PLACA:", xInicio + 3, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.vehiculo.placa}`, xInicio + 25, yPos + 5.5);

        doc.setFont("helvetica", 'bold');
        doc.setTextColor(...azulEtiqueta);
        doc.text("VEHÍCULO:", xInicio + 100, yPos + 5.5);
        doc.setFont("helvetica", 'normal');
        doc.setTextColor(0);
        doc.text(`${data.vehiculo.info}`, xInicio + 125, yPos + 5.5);

        // Ajuste final para la tabla
        let tablaStart = yPos + 12;

        // --- TABLA DE SERVICIOS (Ajustada a 4 columnas) ---
        const rows = data.items.map(item => [
            item.cantidad,
            item.categoria,
            item.descripcion,
            `$${item.precio.toLocaleString('es-CO')}`,
            `$${item.subtotal.toLocaleString('es-CO')}`
        ]);

        doc.autoTable({
            startY: tablaStart,
            head: [['Cant.', 'Categoría', 'Descripción ', 'Precio Unit.', 'Subtotal']],
            body: rows,
            theme: 'grid',
            headStyles: { fillColor: [0, 51, 102], halign: 'center' },
            columnStyles: {
                0: { halign: 'center', cellWidth: 17 },
                1: { halign: 'left', cellWidth: 50},
                2: { halign: 'left', cellWidth: 45},
                3: { halign: 'right', cellWidth: 35 },
                4: { halign: 'right', cellWidth: 35 },
            },
            styles: { fontSize: 9 }
        });

        // --- TOTALES ---
        let finalY = doc.lastAutoTable.finalY + 15;
        doc.setFontSize(12);
        doc.setFont(undefined, 'bold');
        doc.text(`TOTAL A PAGAR: $${data.subtotal_factura.toLocaleString('es-CO')}`, 195, finalY, { align: 'right' });

        doc.save(`Factura_${data.factura_nro}_${data.vehiculo.placa}.pdf`);

    } catch (error) {
        console.error("Error:", error);
        alert("Asegúrate de que el logo esté en /static/AdminLTE/dist/img/logo_taller.png");
    }
}

// Escuchador de clics
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".btn-pdf-factura");
    if (btn) {
        const id = btn.getAttribute("data-id");
        generarPDF(id);
    }
});