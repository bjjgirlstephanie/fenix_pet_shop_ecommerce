# mi_aplication/views.py

from django.shortcuts import render, get_object_or_404
# ⚠️ Importa tus modelos. Si tus modelos están en 'mi_aplication/models.py', usa .models
from .models import Categoria, Producto
# Asumo que la lógica del carrito está en una app llamada 'carrito'
from carrito.carrito import Carrito
from .models import CustomUser
# ----------------------------------------------------------------------
# 1. VISTA DE INICIO (LANDING PAGE)
# ----------------------------------------------------------------------
def home_page(request):
    """
    Muestra la página de inicio con el banner (home.html).
    Necesita el carrito y las categorías para el contexto de base.html.
    """
    # Se obtienen todas las categorías para la barra de navegación (base.html)
    categorias_menu = Categoria.objects.all()
    # Inicializa el carrito para el contexto global
    carrito = Carrito(request)

    context = {
        'categorias_menu': categorias_menu,
        'carrito': carrito
    }
    # Renderiza la plantilla del banner
    return render(request, 'catalogo/home.html', context)


# ----------------------------------------------------------------------
# 2. LISTADO DE TODOS LOS PRODUCTOS
# ----------------------------------------------------------------------
def lista_productos(request):
    """
    Muestra todos los productos disponibles.
    """
    categorias_menu = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    carrito = Carrito(request)

    context = {
        'categorias_menu': categorias_menu,
        'productos': productos,
        'carrito': carrito,
        'categoria_actual': None
    }
    # Renderiza la plantilla con el listado de tarjetas (image_46ddba.png)
    return render(request, 'catalogo/lista_productos.html', context)


# ----------------------------------------------------------------------
# 3. LISTADO DE PRODUCTOS POR CATEGORÍA
# ----------------------------------------------------------------------
def lista_productos_por_categoria(request, slug=None):
    """
    Muestra productos filtrados por una categoría específica.
    """
    categorias_menu = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    carrito = Carrito(request)

    categoria_actual = None
    if slug:
        # Busca la categoría por el slug en la URL
        categoria_actual = get_object_or_404(Categoria, slug=slug)
        productos = productos.filter(categoria=categoria_actual)

    context = {
        'categorias_menu': categorias_menu,
        'productos': productos,
        'carrito': carrito,
        'categoria_actual': categoria_actual
    }
    return render(request, 'catalogo/lista_productos.html', context)


# ----------------------------------------------------------------------
# 4. VISTA DE DETALLE DEL PRODUCTO
# ----------------------------------------------------------------------
def detalle_producto(request, id, slug):
    """
    Muestra el detalle de un solo producto.
    """
    categorias_menu = Categoria.objects.all()
    producto = get_object_or_404(Producto, id=id, slug=slug, disponible=True)
    carrito = Carrito(request)

    context = {
        'categorias_menu': categorias_menu,
        'producto': producto,
        'carrito': carrito,
    }
    return render(request, 'catalogo/detalle_producto.html', context)