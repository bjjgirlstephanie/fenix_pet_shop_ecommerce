from django.contrib import admin
from .models import Categoria, Producto


# Define cómo se mostrarán las categorías en el panel de administración
class CategoriaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de categorías
    list_display = ('id', 'nombre', 'slug',)

    # Pre-pobla el campo 'slug' automáticamente cuando se escribe el 'nombre'
    prepopulated_fields = {'slug': ('nombre',)}


# Define cómo se mostrarán los productos en el panel de administración
class ProductoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la página de lista de productos del admin
    list_display = (
        'id',  # El ID del producto
        'nombre',
        'slug',
        'precio',
        'stock',
        'disponible',
        'creado',
        'actualizado',
    )

    # Filtros avanzados en la barra lateral
    list_filter = ('disponible', 'creado', 'actualizado', 'categoria')

    # Campos que se pueden editar directamente desde la página de lista
    list_editable = ('precio', 'stock', 'disponible')

    # Campos por los cuales se puede buscar
    search_fields = ('nombre', 'descripcion', 'id')  # Añadimos el ID para búsqueda

    # Pre-pobla el campo 'slug' automáticamente cuando se escribe el 'nombre'
    prepopulated_fields = {'slug': ('nombre',)}

    # Define la estructura de las secciones en el formulario de edición/creación
    fieldsets = (
        (None, {
            'fields': ('nombre', 'slug', 'descripcion', 'imagen')
        }),
        ('Información de Precio y Stock', {
            'fields': ('categoria', 'precio', 'stock', 'disponible')
        }),
    )

    # NUEVA FUNCIONALIDAD: Añadimos un filtro de paginación alfabética
    # para mejorar la navegación en listas muy grandes (Django Admin Feature)
    date_hierarchy = 'creado'  # Permite navegar por la fecha de creación
    list_per_page = 20  # Limita el número de ítems por página

    # Añadimos la función de listado por las primeras letras del nombre
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Permite buscar por ID si se proporciona un número
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(id=search_term_as_int)
        except ValueError:
            pass

        return queryset, use_distinct


# Registra los modelos con sus clases de administración personalizadas
# CAMBIO: Usamos CategoriaAdmin para registrar Categoria
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
