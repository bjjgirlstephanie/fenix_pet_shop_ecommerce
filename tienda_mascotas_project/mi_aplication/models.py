# tienda/models.py

from django.db import models
from django.contrib.auth.models import User

class Compra(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.producto} por {self.cliente.username}"
