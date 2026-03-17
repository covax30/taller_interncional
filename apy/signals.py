# apy/signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import DetallePago, DetalleRepuesto, DetalleInsumos

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# HELPER — Persiste la alerta en BD + envía correo
# ══════════════════════════════════════════════════════════════

def _verificar_y_alertar(tipo_item: str, item):
    if not item.stock_bajo:
        return

    nivel = 'sin_stock' if item.stock == 0 else 'stock_bajo'

    from .models import AlertaStock

    alerta_existente = AlertaStock.objects.filter(
        tipo        = tipo_item,
        nombre_item = item.nombre,
        leida       = False,
    ).first()

    if alerta_existente:
        alerta_existente.stock_actual = item.stock
        alerta_existente.nivel        = nivel
        alerta_existente.fecha        = timezone.now()
        alerta_existente.save(update_fields=['stock_actual', 'nivel', 'fecha'])
    else:
        AlertaStock.objects.create(
            tipo         = tipo_item,
            nombre_item  = item.nombre,
            stock_actual = item.stock,
            stock_minimo = item.stock_minimo,
            nivel        = nivel,
        )

    from django.core.cache import cache
    cache_key = f"email_alerta_stock_{tipo_item}_{item.pk}"

    if cache.get(cache_key):
        logger.debug(f"Correo ya enviado recientemente para {tipo_item} #{item.pk}, omitiendo.")
        return

    cache.set(cache_key, True, timeout=7200)
    _enviar_correo_alerta(tipo_item, item.nombre, item.stock, item.stock_minimo)


def _enviar_correo_alerta(tipo_item: str, nombre: str, stock_actual: int, stock_minimo: int):
    destinatarios_raw = getattr(settings, 'ADMINS_CORREO_STOCK', '')
    if not destinatarios_raw:
        logger.warning("ADMINS_CORREO_STOCK no configurado — correo no enviado.")
        return

    destinatarios = [d.strip() for d in destinatarios_raw.split(',') if d.strip()]
    if not destinatarios:
        return

    nivel = "SIN STOCK" if stock_actual == 0 else "STOCK BAJO"
    emoji = "🔴" if stock_actual == 0 else "🟡"
    fecha = timezone.now().strftime("%d/%m/%Y %H:%M")
    color_nivel = "#dc2626" if stock_actual == 0 else "#b45309"
    bg_nivel    = "#fee2e2" if stock_actual == 0 else "#fff3cd"

    asunto = f"{emoji} [{nivel}] {tipo_item}: {nombre} — Taller Internacional de Motores"

    mensaje_texto = (
        f"Alerta de Inventario — {fecha}\n\n"
        f"{emoji} {nivel}\n\n"
        f"Tipo     : {tipo_item}\n"
        f"Ítem     : {nombre}\n"
        f"Stock    : {stock_actual} unidades\n"
        f"Mínimo   : {stock_minimo} unidades\n\n"
        f"Por favor, gestione el reabastecimiento a la brevedad.\n\n"
        f"---\nSistema de Gestión — Taller Internacional de Motores"
    )

    mensaje_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style>
    body      {{ font-family:Arial,sans-serif; background:#f4f4f4; margin:0; padding:20px; }}
    .card     {{ background:#fff; border-radius:8px; padding:30px; max-width:520px;
                 margin:auto; box-shadow:0 2px 12px rgba(0,0,0,.1); }}
    .header   {{ text-align:center; margin-bottom:24px; }}
    .badge    {{ display:inline-block; padding:6px 18px; border-radius:20px;
                 font-weight:bold; font-size:1rem; background:{bg_nivel}; color:{color_nivel}; }}
    table     {{ width:100%; border-collapse:collapse; margin:20px 0; }}
    td        {{ padding:10px 14px; border-bottom:1px solid #f0f0f0; font-size:.95rem; }}
    td:first-child {{ font-weight:bold; color:#555; width:35%; }}
    .footer   {{ text-align:center; color:#9ca3af; font-size:.78rem; margin-top:24px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div style="font-size:2.5rem;margin-bottom:8px;">{emoji}</div>
      <span class="badge">{nivel}</span>
      <h2 style="margin:12px 0 4px;color:#111;">Alerta de Inventario</h2>
      <small style="color:#6b7280;">{fecha}</small>
    </div>
    <table>
      <tr><td>Tipo</td><td>{tipo_item}</td></tr>
      <tr><td>Ítem</td><td><strong>{nombre}</strong></td></tr>
      <tr><td>Stock actual</td>
          <td style="color:{color_nivel};font-weight:bold;">{stock_actual} unidades</td></tr>
      <tr><td>Stock mínimo</td><td>{stock_minimo} unidades</td></tr>
    </table>
    <p style="color:#374151;font-size:.92rem;text-align:center;">
      Por favor, gestione el reabastecimiento a la brevedad.
    </p>
    <div class="footer">
      Sistema de Gestión · Taller Internacional de Motores<br>
      Mensaje generado automáticamente — no responder.
    </div>
  </div>
</body>
</html>
    """.strip()

    try:
        send_mail(
            subject        = asunto,
            message        = mensaje_texto,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = destinatarios,
            html_message   = mensaje_html,
            fail_silently  = False,
        )
        logger.info(f"Correo de alerta enviado: {tipo_item} '{nombre}' → {destinatarios}")
    except Exception as exc:
        logger.error(f"Error al enviar correo de alerta para '{nombre}': {exc}")


# ══════════════════════════════════════════════════════════════
# SEÑALES — PAGOS (compra a proveedor → SUMA stock + actualiza precio)
# ══════════════════════════════════════════════════════════════

@receiver(post_save, sender=DetallePago)
def sumar_stock_al_comprar(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        if instance.tipo_item == 'Repuesto' and instance.repuesto:
            rep = instance.repuesto
            rep.stock += instance.cantidad
            rep.precio_unitario = instance.precio_unitario  # ← actualiza precio con último costo
            rep.save(update_fields=['stock', 'precio_unitario'])

        elif instance.tipo_item == 'Insumo' and instance.insumo:
            ins = instance.insumo
            ins.stock += instance.cantidad
            ins.costo = instance.precio_unitario  # ← actualiza costo del insumo
            ins.save(update_fields=['stock', 'costo'])

        elif instance.tipo_item == 'Herramienta' and instance.herramienta:
            her = instance.herramienta
            her.stock += instance.cantidad
            her.save(update_fields=['stock'])


@receiver(post_delete, sender=DetallePago)
def restar_stock_al_anular_compra(sender, instance, **kwargs):
    with transaction.atomic():
        if instance.tipo_item == 'Repuesto' and instance.repuesto:
            rep = instance.repuesto
            rep.stock = max(0, rep.stock - instance.cantidad)
            rep.save(update_fields=['stock'])

        elif instance.tipo_item == 'Insumo' and instance.insumo:
            ins = instance.insumo
            ins.stock = max(0, ins.stock - instance.cantidad)
            ins.save(update_fields=['stock'])

        elif instance.tipo_item == 'Herramienta' and instance.herramienta:
            her = instance.herramienta
            her.stock = max(0, her.stock - instance.cantidad)
            her.save(update_fields=['stock'])


# ══════════════════════════════════════════════════════════════
# SEÑALES — DETALLE SERVICIO (uso en servicio → RESTA stock + alerta)
# ══════════════════════════════════════════════════════════════

@receiver(post_save, sender=DetalleRepuesto)
def restar_stock_repuesto_en_servicio(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        repuesto = instance.id_repuesto
        repuesto.stock = max(0, repuesto.stock - instance.cantidad)
        repuesto.save(update_fields=['stock'])

    repuesto.refresh_from_db()
    _verificar_y_alertar('Repuesto', repuesto)


@receiver(post_delete, sender=DetalleRepuesto)
def devolver_stock_repuesto_al_cancelar_servicio(sender, instance, **kwargs):
    with transaction.atomic():
        repuesto = instance.id_repuesto
        repuesto.stock += instance.cantidad
        repuesto.save(update_fields=['stock'])

    repuesto.refresh_from_db()
    if not repuesto.stock_bajo:
        from .models import AlertaStock
        AlertaStock.objects.filter(
            tipo='Repuesto', nombre_item=repuesto.nombre, leida=False
        ).update(leida=True)


@receiver(post_save, sender=DetalleInsumos)
def restar_stock_insumo_en_servicio(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        insumo = instance.id_insumos
        insumo.stock = max(0, insumo.stock - instance.cantidad)
        insumo.save(update_fields=['stock'])

    insumo.refresh_from_db()
    _verificar_y_alertar('Insumo', insumo)


@receiver(post_delete, sender=DetalleInsumos)
def devolver_stock_insumo_al_cancelar_servicio(sender, instance, **kwargs):
    with transaction.atomic():
        insumo = instance.id_insumos
        insumo.stock += instance.cantidad
        insumo.save(update_fields=['stock'])

    insumo.refresh_from_db()
    if not insumo.stock_bajo:
        from .models import AlertaStock
        AlertaStock.objects.filter(
            tipo='Insumo', nombre_item=insumo.nombre, leida=False
        ).update(leida=True)