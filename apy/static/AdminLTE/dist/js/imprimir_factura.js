document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-pdf-factura").forEach(btn => {
        btn.addEventListener("click", () => {

            const factura = {
                id: btn.dataset.id,
                fecha: btn.dataset.fecha,
                cliente: btn.dataset.cliente,
                documento: btn.dataset.documento,
                empleado: btn.dataset.empleado,
                empresa: btn.dataset.empresa,
                metodoPago: btn.dataset.metodoPago,
                monto: btn.dataset.monto,
            };

            generarPDFFactura(factura);
        });
    });
});

function generarPDFFactura(factura) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Título
    doc.setFontSize(16);
    doc.text(`Factura #${factura.id}`, 20, 20);

    // Contenido
    doc.setFontSize(11);
    doc.text(`Fecha: ${factura.fecha}`, 20, 30);
    doc.text(`Empresa: ${factura.empresa}`, 20, 40);
    doc.text(`Cliente: ${factura.cliente} (${factura.documento})`, 20, 50);
    doc.text(`Empleado: ${factura.empleado}`, 20, 60);
    doc.text(`Método de pago: ${factura.metodoPago}`, 20, 70);
    doc.text(`Monto total: $${factura.monto}`, 20, 80);

    // 👉 SOLO descarga el PDF
    doc.save(`Factura_${factura.id}.pdf`);
}
