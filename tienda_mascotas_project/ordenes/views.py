# ordenes/views.py
import stripe
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrdenCreateForm
from .models import Orden, ItemOrden
from carrito.carrito import Carrito
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal

# Inicializar Stripe con la clave secreta
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.contrib.auth.decorators import login_required


@login_required
def mis_pedidos_view(request):
    """Muestra la lista de órdenes realizadas por el usuario logueado."""
    # Si guardas las órdenes asociadas al usuario:
    ordenes = Orden.objects.filter(email=request.email) if hasattr(request, 'email') else Orden.objects.all()

    # O si usas el modelo de usuario de Django:
    # ordenes = Orden.objects.filter(user=request.user)

    return render(request, 'ordenes/mis_pedidos.html', {'ordenes': ordenes})


def obtener_total_orden(orden):
    """Función de apoyo para obtener el total de la orden de forma segura."""
    for campo in ['total_final', 'total', 'monto_total']:
        if hasattr(orden, campo):
            val = getattr(orden, campo)
            if val is not None:
                return Decimal(str(val))
    return Decimal('0.00')


def procesar_pago_exitoso(orden):
    """Función auxiliar para marcar la orden como pagada y enviar el correo de éxito."""
    orden.estado = "PAGADA"
    if hasattr(orden, 'pagado'):
        orden.pagado = True
    orden.save()

    try:
        subtotal = sum(item.precio * item.cantidad for item in orden.items.all())
        iva = subtotal * Decimal("0.19")  # ✔️ Corregido
        total_final_email = subtotal + iva

        html_message = render_to_string('ordenes/orden_confirmada.html', {
            'orden': orden,
            'orden_id': orden.id,
            'orden_items': orden.items.all(),
            'subtotal': subtotal,
            'iva': iva,
            'total_final': total_final_email,
        })
        plain_message = strip_tags(html_message)

        send_mail(
            'Confirmación de Orden Pagada #{}'.format(orden.id),
            plain_message,
            'ep847020@gmail.com',
            [orden.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error al enviar correo: {e}")


def procesar_orden_pendiente(orden):
    """Envía el correo de orden creada con estado pendiente (para contraentrega)."""
    orden.estado = "PENDIENTE"
    if hasattr(orden, 'pago contraentrega'):
        orden.pagado = False
    orden.save()

    try:
        subtotal = sum(item.precio * item.cantidad for item in orden.items.all())
        iva = subtotal * Decimal("0.19")
        total_final_email = subtotal + iva

        html_message = render_to_string('ordenes/orden_confirmada.html', {
            'orden': orden,
            'orden_id': orden.id,
            'orden_items': orden.items.all(),
            'subtotal': subtotal,
            'iva': iva,
            'total_final': total_final_email,
        })
        plain_message = strip_tags(html_message)

        send_mail(
            'Resumen de Orden Pendiente #{}'.format(orden.id),
            plain_message,
            'ep847020@gmail.com',
            [orden.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error al enviar correo pendiente: {e}")


def orden_confirmacion(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)

    # 1. Asegurar que si la orden no tiene total_final, se calcule de inmediato de sus items
    total_final = obtener_total_orden(orden)
    if total_final == Decimal('0.00') or total_final is None:
        total_final = sum(item.precio * item.cantidad for item in orden.items.all())
        orden.total_final = total_final
        orden.save()

    subtotal = total_final / Decimal("1.19")
    iva = subtotal * Decimal("0.19")

    return render(request, 'ordenes/orden_confirmada.html', {
        'orden': orden,
        'orden_id': orden.id,
        'cliente_email': orden.email,
        'orden_items': orden.items.all(),
        'subtotal': subtotal,
        'iva': iva,
        'total_final': total_final
    })
def orden_create(request):
    carrito = Carrito(request)

    if not carrito:
        return redirect('catalogo:lista_productos')

    if request.method == 'POST':
        form = OrdenCreateForm(request.POST)
        if form.is_valid():
            # 1. Crear la Orden
            orden = form.save(commit=False)
            orden.total_final = carrito.get_precio_total()

            metodo_pago = request.POST.get("metodo_pago")
            orden.metodo_pago = metodo_pago
            orden.estado = "PENDIENTE"
            orden.save()

            # 2. Guardar los ítems de la orden
            for item in carrito:
                ItemOrden.objects.create(
                    orden=orden,
                    producto=item['producto'],
                    precio=item['precio'],
                    cantidad=item['cantidad']
                )

            # 3. Vaciar el carrito
            carrito.clear()

            # 4. Flujo según método de pago elegido
            if metodo_pago == "TARJETA_PASARELA":
                return redirect('ordenes:simular_tarjeta', orden_id=orden.id)

            elif metodo_pago == "MANUAL_TRANSFERENCIA":
                return redirect('ordenes:simular_nequi', orden_id=orden.id)

            elif metodo_pago == "CONTRAENTREGA":
                procesar_orden_pendiente(orden)
                return redirect('ordenes:pago_contraentrega', orden_id=orden.id)

    else:
        form = OrdenCreateForm()

    return render(request, 'ordenes/crear.html', {
        'carrito': carrito,
        'form': form,
    })


def simular_pago_nequi(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    total_final = obtener_total_orden(orden)

    # Si por alguna razón la orden no tenía total_final guardado, se lo asignamos
    if total_final == Decimal('0.00'):
        total_final = sum(item.precio * item.cantidad for item in orden.items.all())
        orden.total_final = total_final
        orden.save()

    subtotal = total_final / Decimal("1.19")
    iva = subtotal * Decimal("0.19")

    if request.method == "POST":
        # Forzamos la actualización directa del estado en la base de datos
        orden.estado = "PAGADA"
        if hasattr(orden, 'pagado'):
            orden.pagado = True
        orden.save()

        # Enviamos correo y mensaje de éxito
        procesar_pago_exitoso(orden)
        messages.success(request,
                         "¡Transacción Nequi aprobada exitosamente! Te hemos enviado un correo de confirmación.")
        return redirect('ordenes:orden_confirmada', orden_id=orden.id)

    return render(request, "ordenes/simular_nequi.html", {
        "orden": orden,
        "orden_id": orden.id,
        "total_final": total_final,
        "subtotal": subtotal,
        "iva": iva,
    })


def simular_tarjeta_view(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    total_final = obtener_total_orden(orden)

    # Si el total viene vacío o en cero, lo calculamos de sus ítems de inmediato
    if total_final == Decimal('0.00') or total_final is None:
        total_final = sum(item.precio * item.cantidad for item in orden.items.all())
        orden.total_final = total_final
        orden.save()

    subtotal = total_final / Decimal("1.19")
    iva = subtotal * Decimal("0.19")

    if request.method == "POST":
        procesar_pago_exitoso(orden)
        messages.success(request, "¡Pago con tarjeta procesado con éxito! Revisa tu correo electrónico.")
        return redirect('ordenes:orden_confirmada', orden_id=orden.id)

    return render(request, "ordenes/simular_tarjeta.html", {
        "orden": orden,
        "orden_id": orden.id,
        "total_final": total_final,
        "subtotal": subtotal,
        "iva": iva,
    })


def cancelar_orden_view(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)

    if request.method == "POST":
        if orden.puede_cancelar():
            orden.estado = "CANCELADO"
            orden.save()
            messages.success(request, f"La Orden #{orden.id} ha sido cancelada exitosamente.")
        else:
            messages.error(request, "Lo sentimos, el tiempo límite de 5 horas para cancelar esta orden ha expirado.")

    return redirect('ordenes:orden_confirmada', orden_id=orden.id)


def orden_detalle_html(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    return render(request, 'ordenes/orden_detalle.html', {'orden': orden})


def pago_pendiente(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    total_final = obtener_total_orden(orden)
    subtotal = total_final / Decimal("1.19")
    iva = subtotal * Decimal("0.19")  # ✔️ Corregido

    return render(request, 'ordenes/pago_contraentrega.html', {
        'orden': orden,
        'orden_id': orden.id,
        'monto_total': total_final,
        'moneda': 'COP',
        'instrucciones': 'Tu pedido será pagado en efectivo al momento de la entrega en tu domicilio.'
    })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    WEBHOOK_SECRET = 'whsec_testing_1234'

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        orden_id = session.metadata.get('orden_id')

        try:
            orden = Orden.objects.get(id=orden_id)
        except Orden.DoesNotExist:
            return HttpResponse(status=404)

        if orden.estado != 'PAGADA':
            procesar_pago_exitoso(orden)

    return HttpResponse(status=200)