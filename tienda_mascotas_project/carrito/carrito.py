# carrito/carrito.py

from decimal import Decimal
from django.conf import settings
from catalogo.models import Producto




class Carrito:
    def __init__(self, request):
        """Inicializar el carrito."""
        self.session = request.session
        # Obtener el diccionario de carrito de la sesión o inicializar uno vacío
        carrito = self.session.get(settings.CARRITO_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CARRITO_SESSION_ID] = {}
        self.carrito = carrito

    def add(self, producto, cantidad=1, actualizar_cantidad=True):
        """
        Añade un producto al carrito o actualiza su cantidad.
        """
        producto_id = str(producto.id)

        # 1. Validación de Inventario antes de añadir/actualizar
        if producto.stock < cantidad and not actualizar_cantidad:
            # Si no está actualizando y la cantidad solicitada excede el stock
            raise ValueError("No hay suficiente stock disponible para la cantidad solicitada.")

        if producto_id not in self.carrito:
            # Si el producto es nuevo en el carrito
            self.carrito[producto_id] = {'cantidad': 0,
                                      'precio': str(producto.precio)}

        if actualizar_cantidad:
            # Si se está actualizando explícitamente (ej. en la vista detalle)
            self.carrito[producto_id]['cantidad'] = cantidad
        else:
            # Si se está añadiendo una cantidad (ej. desde el catálogo)
            self.carrito[producto_id]['cantidad'] += cantidad

        # 2. Verificación final de stock después de la operación
        if self.carrito[producto_id]['cantidad'] > producto.stock:
            # Si la cantidad total en el carrito excede el stock, ajustarla al máximo
            self.carrito[producto_id]['cantidad'] = producto.stock
            # Aquí podrías levantar una advertencia al usuario si fuera necesario

        self.save()

    def save(self):
        """Marcar la sesión como 'modificada' para asegurar que se guarde."""
        self.session.modified = True

    def remove(self, producto):
        """Eliminar un producto del carrito."""
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.session.modified = True
            self.save()

    def __iter__(self):
        """
        Itera sobre los ítems en el carrito y obtiene los productos
        de la base de datos.
        """
        producto_ids = self.carrito.keys()
        # Obtiene objetos Producto y los mapea a sus IDs
        productos = Producto.objects.filter(id__in=producto_ids)

        carrito = self.carrito.copy()
        for producto in productos:
            carrito_item = carrito[str(producto.id)]
            carrito_item['producto'] = producto
            carrito_item['precio'] = Decimal(carrito_item['precio'])
            carrito_item['total_precio'] = carrito_item['precio'] * carrito_item['cantidad']
            yield carrito_item

    def __len__(self):
        """
        Cuenta el número total de ítems en el carrito.
        """
        return sum(item['cantidad'] for item in self.carrito.values())


    def get_precio_total(self):
        """Calcular el costo total de los ítems en el carrito."""
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())

    def clear(self):
        """Vaciar el carrito de la sesión."""
        del self.session[settings.CARRITO_SESSION_ID]
        self.save()


    def get_total_items(self):
        """
        Devuelve el número total de productos únicos en el carrito.
        """
        return len(self.carrito)

    def get_cantidad(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            return int(self.carrito[producto_id]['cantidad'])
        return 0