from .carrito import Carrito

def carrito(request):
    """
    Este context processor añade la variable 'cart' (el objeto Cart)
    al contexto de todas las plantillas, haciéndola accesible globalmente.
    """
    return {'carrito': Carrito(request)}