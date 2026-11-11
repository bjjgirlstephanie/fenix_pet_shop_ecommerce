# catalogo/urls.py
from .views import nutricalculadora_view
from django.urls import path
from .views import ListaProductos, DetalleProducto  # <-- Importamos las vistas
from . import views

app_name = 'catalogo'

urlpatterns = [
# ListaProductos.as_view() es necesario porque es una Clase, no una función
    path('', views.ListaProductos.as_view(), name='lista_productos'),
    # 2. NUEVA RUTA DE FILTRO: captura el slug de la categoría
    path('categoria/<slug:slug>/', ListaProductos.as_view(), name='lista_productos_por_categoria'),


    # 3. Ruta de detalle de producto
    # catalogo/urls.py
    path('producto/<int:pk>/', DetalleProducto.as_view(), name='detalle_producto'),

  # 2. URL de productos filtrados por categoría (ej. /accesorios-gatos/)
    path('<slug:slug>/', ListaProductos.as_view(), name='lista_productos_por_categoria'),
    path('favorito/toggle/<int:producto_id>/', views.toggle_favorito, name='toggle_favorito'),

    path('nutricalculadora/<int:producto_id>//', views.nutricalculadora_view, name='nutricalculadora'),


]