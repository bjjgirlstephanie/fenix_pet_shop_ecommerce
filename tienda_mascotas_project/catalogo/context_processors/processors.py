# catalogo/context_processors/processors.py
from ..models import Categoria

def categorias_visibles(request):
    # Obtiene todas las categorías para mostrarlas en el menú
    return {'categorias_menu': Categoria.objects.all()}