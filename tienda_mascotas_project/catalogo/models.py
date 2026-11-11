
# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model


# Obtiene el modelo de usuario activo para evitar dependencias circulares
User = settings.AUTH_USER_MODEL



class Categoria(models.Model):
    # Nombre de la categoría (ej: Alimento para Perros, Juguetes para Gatos)
    nombre = models.CharField(max_length=200, db_index=True)

    # Slug para URLs amigables (ej: /categoria/alimento-para-perros)
    # unique=True asegura que no haya dos slugs iguales.
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        # Nombre singular y plural para el panel de administración
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        # Ordenar alfabéticamente
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

    # Opcional: Función para obtener la URL de la categoría (útil para el frontend)
    # def get_absolute_url(self):
    #     return reverse('catalogo:lista_productos_por_categoria', args=[self.slug])


class Producto(models.Model):
    # Relación uno a muchos: Un producto pertenece a UNA categoría.
    # on_delete=models.CASCADE: Si eliminas la categoría, se eliminan los productos asociados.
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)

    # Información básica
    nombre = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del producto")


    # Media: Se guardarán las rutas a las imágenes.
    # Necesitarás la librería Pillow (pip install Pillow) para usar ImageField en producción.
    imagen = models.ImageField(upload_to='productos', blank=True)

    # Precios y Stock
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # 99,999,999.99
    stock = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    # Tiempos
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    #campos nutricionales calculadora
    calorias_por_porcion = models.FloatField(default=0, help_text="Kcal por porción/taza")
    proteinas = models.FloatField(default=0, help_text="Gramos de proteína")
    grasas = models.FloatField(default=0, help_text="Gramos de grasa")
    carbohidratos = models.FloatField(default=0, help_text="Gramos de carbohidratos")

    def __str__(self):
        return f"{self.nombre} ({self.marca})"



    class Meta:
        # Índice combinado para búsquedas rápidas (por ID y slug)

        ordering = ('nombre',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]


    def __str__(self):
        return self.nombre

    # Función para obtener la URL del detalle del producto
    def get_absolute_url(self):
        # Asume que tendrás una ruta llamada 'producto_detalle' en tu aplicación 'catalogo'
        return reverse('catalogo:detalle_producto', args=[self.id, self.slug])




# Obtener el modelo de usuario activo en Django
User = get_user_model()

# ... (Tus clases Producto y Categoria existentes aquí) ...
''' 
class Favorito(models.Model):
    """
    Asocia un usuario con un producto que ha marcado como favorito.
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey(Producto, related_name='favoritos', on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Asegura que un usuario solo pueda tener un producto como favorito una vez
        unique_together = ('usuario', 'producto')
        verbose_name = 'favorito'
        verbose_name_plural = 'favoritos'

    def __str__(self):
        return f'{self.usuario.username} likes {self.producto.nombre}'
'''