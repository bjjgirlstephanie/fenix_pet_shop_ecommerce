from django.db import models
from catalogo.models import Producto

class Orden(models.Model):
    # 1. Información de Usuario (opcional)
    usuario = models.ForeignKey(
        'auth.User',
        related_name='ordenes',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 2. Información del Cliente / Envío
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    direccion = models.CharField(max_length=250)
    codigo_postal = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)

    # 3. Datos de Pago
    OPCIONES_PAGO = [
        ('MANUAL_TRANSFERENCIA', 'NEQUI / Transferencia Bancaria'),
        ('TARJETA_PASARELA', 'Tarjeta de Crédito / Débito (Pasarela)'),
        ('CONTRAENTREGA', 'Pago Contra Entrega'),
    ]
    metodo_pago = models.CharField(
        max_length=20,
        choices=OPCIONES_PAGO,
        default='MANUAL_TRANSFERENCIA'
    )

    # 4. Datos de la Transacción y Estado
    ESTADO_CHOICES = [
        ('CREADA', 'Orden Creada'),
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
        ('PAGADA', 'Pago Confirmado'),
        ('ENVIADA', 'Enviada'),
        ('CANCELADA', 'Cancelada'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE_PAGO'
    )

    pagado = models.BooleanField(default=False)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # 5. Fechas
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-creado',)
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'

    def __str__(self):
        return f'Orden {self.id}'

    def get_total_cost(self):
        """Calcula el costo total sumando los ítems."""
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        """
        Ajusta automáticamente el estado y el campo 'pagado'
        según el método de pago seleccionado.
        """
        if self.metodo_pago == "TARJETA_PASARELA":
            self.estado = "PAGADA"
            self.pagado = True
        elif self.metodo_pago == "MANUAL_TRANSFERENCIA":
            self.estado = "PENDIENTE_PAGO"
            self.pagado = False
        elif self.metodo_pago == "CONTRAENTREGA":
            self.estado = "PENDIENTE_PAGO"
            self.pagado = False

        super().save(*args, **kwargs)

# --- Clase ItemOrden (Debe estar inmediatamente después de Orden) ---

class ItemOrden(models.Model):
    # Relaciona el ítem con una Orden
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)

    # El producto que fue comprado
    producto = models.ForeignKey(Producto, related_name='orden_items', on_delete=models.CASCADE)

    # Precio fijo al momento de la compra
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Cantidad
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Ítem de Orden'
        verbose_name_plural = 'Ítems de Orden'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.precio * self.cantidad


