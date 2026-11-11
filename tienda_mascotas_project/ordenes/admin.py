
# Register your models here.
# ordenes/admin.py
from django.contrib import admin
from .models import Orden, ItemOrden

# 1. Definir cómo se verán los ítems de la orden
# Usamos StackedInline o TabularInline para mostrar los ítems dentro de la Orden
class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    # Campos que se pueden editar directamente en el panel de la Orden
    fields = ['producto', 'precio', 'cantidad']
    # Evita que se añadan filas vacías por defecto
    extra = 0
    # Hace que el precio y cantidad solo sean de lectura (ya que se fijan al crear la orden)
    readonly_fields = ['producto', 'precio', 'cantidad']


# 2. Definir cómo se verá la Orden principal
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nombre', 'apellido', 'email', 'monto_total',
        'metodo_pago', 'estado', 'creado', 'actualizado'
    ]
    # Filtros laterales
    list_filter = ['estado', 'metodo_pago', 'creado', 'actualizado']
    # Campos de solo lectura (no deben cambiarse después de la creación)
    readonly_fields = ['monto_total', 'creado', 'actualizado']
    # Para ver los ítems de la orden dentro de la orden principal
    inlines = [ItemOrdenInline]
    # Buscador
    search_fields = ['id', 'nombre', 'apellido', 'email']