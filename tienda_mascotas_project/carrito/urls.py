# carrito/urls.py

from . import views
from django.urls import path, include  # ⬅️ ¡AÑADE 'include' AQUÍ!
from catalogo.views import home_page


app_name = 'carrito'

urlpatterns = [
    path('detalle', views.carrito_detalle, name='carrito_detalle'),
    path('agregar/<int:producto_id>/', views.carrito_add, name='carrito_add'),
# Ejemplo en carrito/urls.py
    path('elimar/<int:producto_id>/', views.carrito_remove, name='carrito_remove'),
    path('vaciar/', views.carrito_clear, name='carrito_clear'),

]