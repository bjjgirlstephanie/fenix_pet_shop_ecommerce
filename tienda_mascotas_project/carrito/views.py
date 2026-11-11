from catalogo.models import Producto
from django.contrib.auth.decorators import login_required
from .carrito import Carrito
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CarritoAddProductoForm
from django.contrib import messages


@login_required(login_url='account_login')
def carrito_add(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    # ✅ Si viene desde catálogo o detalle, agregar 1 unidad
    if request.method == "POST" and "accion" not in request.POST:
        carrito.add(producto=producto, cantidad=1, actualizar_cantidad=False)
        messages.success(request, f"{producto.nombre} agregado al carrito.")
        return redirect(request.META.get('HTTP_REFERER', 'catalogo:lista_productos'))

    # ✅ Si viene desde botones + / - del carrito
    accion = request.POST.get("accion")
    if accion:
        cantidad_actual = carrito.get_cantidad(producto) if hasattr(carrito, 'get_cantidad') else 1
        if accion == "sumar":
            nueva_cantidad = cantidad_actual + 1
        elif accion == "restar":
            nueva_cantidad = max(1, cantidad_actual - 1)
        else:
            nueva_cantidad = cantidad_actual

        carrito.add(producto=producto, cantidad=nueva_cantidad, actualizar_cantidad=True)
        return redirect("carrito:carrito_detalle")

    return redirect(request.META.get('HTTP_REFERER', 'catalogo:lista_productos'))


@require_POST
def carrito_remove(request, producto_id):
    """
    Función para eliminar un producto del carrito.
    Solo acepta peticiones POST.
    """
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    carrito.remove(producto)
    messages.warning(request, f"{producto.nombre} eliminado del carrito.")

    return redirect('carrito:carrito_detalle')


def carrito_detalle(request):
    carrito = Carrito(request)
    items = []

    # Manejo seguro por si el carrito usa un diccionario o una lista interna
    carrito_items = getattr(carrito, 'carrito', carrito)

    for producto_id, item in carrito_items.items():
        producto = get_object_or_404(Producto, id=producto_id)
        items.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio': item['precio'],
        })
    return render(request, 'carrito/detalle.html', {'items': items, 'carrito': carrito})


def carrito_clear(request):
    """
    Vista para vaciar completamente el carrito.
    """
    carrito = Carrito(request)
    carrito.clear()

    messages.info(request, "El carrito de compras ha sido vaciado.")
    return redirect('carrito:carrito_detalle')