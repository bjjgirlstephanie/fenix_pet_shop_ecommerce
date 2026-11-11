# ordenes/urls.py (Actualizado)
from django.urls import path
from . import views


app_name = 'ordenes'
urlpatterns = [
    path('crear/', views.orden_create, name='orden_create'),
    path('confirmada/<int:orden_id>/', views.orden_confirmacion, name='orden_confirmada'),
    path('simular-tarjeta/<int:orden_id>/', views.simular_tarjeta_view, name='simular_tarjeta'),
    path('simular-nequi/<int:orden_id>/', views.simular_pago_nequi, name='simular_nequi'),
    path('pago-contraentrega/<int:orden_id>/', views.pago_pendiente, name='pago_contraentrega'),
    path('cancelar/<int:orden_id>/', views.cancelar_orden_view, name='cancelar_orden'),

    path('mis-pedidos/', views.mis_pedidos_view, name='mis_pedidos'),

]