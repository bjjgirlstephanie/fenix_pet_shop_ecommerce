# catalogo/views.py
from django.views.generic import ListView, DetailView
from django.views import View
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Producto, Categoria
from carrito.forms import CarritoAddProductoForm
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404  # <--- Asegúrate de tener get_object_or_404 aquí


stripe.api_key = settings.STRIPE_SECRET_KEY


# Vista para listar productos
class ListaProductos(ListView):
    model = Producto
    template_name = 'catalogo/lista_productos.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        # 1. Empieza con todos los productos disponibles
        queryset = Producto.objects.filter(disponible=True)

        # 2. Manejar la búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | Q(descripcion__icontains=query)
            )

        # 3. Manejar filtro por categoría
        category_slug = self.kwargs.get('slug')
        if category_slug:
            try:
                category = Categoria.objects.get(slug=category_slug)
                queryset = queryset.filter(categoria=category)
                self.current_category = category
            except Categoria.DoesNotExist:
                self.current_category = None
        else:
            self.current_category = None

        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar la categoría actual
        context['current_category'] = getattr(self, 'current_category', None)
        # Pasar todas las categorías
        context['categorias'] = Categoria.objects.all()
        # Pasar el formulario del carrito
        context['carrito_producto_form'] = CarritoAddProductoForm()
        return context

    # Permitir solicitudes POST desde el catálogo (Nutricalculadora general)
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        resultado_nutricional = None
        tipo_mascota = None

        if request.POST.get('accion') == 'nutricalcular':
            try:
                tipo_mascota = request.POST.get('tipo_mascota')
                peso = float(request.POST.get('peso', 0))
                actividad = request.POST.get('actividad', 'normal')

                factor = 1.2
                if actividad == 'baja':
                    factor = 1.0
                elif actividad == 'alta':
                    factor = 1.4

                rer = 70 * (peso ** 0.75)
                resultado_nutricional = rer * factor
            except ValueError:
                pass

        context.update({
            'resultado_nutricional': round(resultado_nutricional, 1) if resultado_nutricional else None,
            'tipo_mascota': tipo_mascota,
        })

        return self.render_to_response(context)



# Vista para el detalle de un solo producto
class DetalleProducto(DetailView):
    model = Producto
    template_name = 'catalogo/detalle_productos.html'
    context_object_name = 'producto'

    def get_queryset(self):
        return Producto.objects.filter(disponible=True)


# Vista para la página de inicio
def home_page(request):
    """Muestra la página de inicio con el banner."""
    return render(request, 'catalogo/home.html')



# ordenes/views.py



class CrearCheckoutView(View):
    def post(self, request, *args, **kwargs):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Producto de prueba',
                    },
                    'unit_amount': 2000,  # en centavos (20 USD)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/ordenes/success/',
            cancel_url='http://127.0.0.1:8000/ordenes/cancel/',
        )
        return redirect(session.url)


# Vistas para mostrar resultado del pago
def success(request):
    return render(request, "ordenes/mostrarPasarela.html")

def cancel(request):
    return render(request, "ordenes/cancel.html")


@login_required
def toggle_favorito(request, producto_id):
    """
    Añade o elimina un producto de la lista de favoritos del usuario actual.
    """
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        usuario = request.user

        # Intenta obtener el favorito existente
        favorito_existente = Favorito.objects.filter(usuario=usuario, producto=producto)

        if favorito_existente.exists():
            # Si ya es favorito, lo eliminamos
            favorito_existente.delete()
            return JsonResponse({'status': 'eliminado', 'is_favorito': False})
        else:
            # Si no es favorito, lo añadimos
            Favorito.objects.create(usuario=usuario, producto=producto)
            return JsonResponse({'status': 'agregado', 'is_favorito': True})

    return HttpResponseBadRequest("Método no permitido. Solo POST.")


# Nutricalculadora por producto específico
def nutricalculadora_view(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    calorias_recomendadas = 0
    gramos_diarios = 0
    tazas_diarias = 0
    proteinas_g = 0
    grasas_g = 0
    carbs_g = 0
    calculado = False
    perfil_seleccionado = ""

    if request.method == 'POST':
        try:
            peso = float(request.POST.get('peso', 0))
            tipo_mascota = request.POST.get('tipo_mascota', 'perro')
            etapa_tamano = request.POST.get('etapa_tamano', 'adulto_normal')

            # 1. Cálculo de RER (Requerimiento Energético en Reposo)
            rer = 70 * (peso ** 0.75)

            # 2. Factores multiplicadores según la etapa, tamaño y especie
            factor_multiplicador = 1.2  # Por defecto

            if tipo_mascota == 'perro':
                if etapa_tamano == 'cachorro_pequeno':
                    factor_multiplicador = 3.0  # Los cachorros pequeños consumen mucha más energía por kg
                elif etapa_tamano == 'cachorro_grande':
                    factor_multiplicador = 2.5
                elif etapa_tamano == 'adulto_pequeno':
                    factor_multiplicador = 1.4  # Razas miniatura/pequeñas suelen tener metabolismo más acelerado
                elif etapa_tamano == 'adulto_mediano':
                    factor_multiplicador = 1.6
                elif etapa_tamano == 'adulto_grande':
                    factor_multiplicador = 1.3  # Razas grandes tienden a ser un poco más tranquilas
                elif etapa_tamano == 'senior':
                    factor_multiplicador = 1.1
                elif etapa_tamano == 'esterilizado':
                    factor_multiplicador = 1.0
            else:  # Gatos
                if etapa_tamano == 'gato_cachorro':
                    factor_multiplicador = 2.5
                elif etapa_tamano == 'gato_adulto':
                    factor_multiplicador = 1.2  # Adulto esterilizado/normal
                elif etapa_tamano == 'gato_senior':
                    factor_multiplicador = 1.0

            calorias_recomendadas = rer * factor_multiplicador

            # 3. Dosificación exacta en gramos basada en el producto
            # Usamos el campo del producto si existe, o un estándar de 3.5 kcal/g
            kcal_por_gramo = getattr(producto, 'kcal_por_gramo', 3.5)
            if not kcal_por_gramo or kcal_por_gramo <= 0:
                kcal_por_gramo = 3.5

            gramos_diarios = calorias_recomendadas / kcal_por_gramo
            tazas_diarias = gramos_diarios / 100  # 1 taza estándar aprox. 100g

            # 4. Distribución de macronutrientes orientativa
            proteinas_g = (calorias_recomendadas * 0.30) / 4
            grasas_g = (calorias_recomendadas * 0.25) / 9
            carbs_g = (calorias_recomendadas * 0.45) / 4

            calculado = True
            perfil_seleccionado = etapa_tamano
        except ValueError:
            pass

    context = {
        'producto': producto,
        'calorias_recomendadas': round(calorias_recomendadas, 1),
        'gramos_diarios': round(gramos_diarios, 0),
        'tazas_diarias': round(tazas_diarias, 1),
        'proteinas_g': round(proteinas_g, 1),
        'grasas_g': round(grasas_g, 1),
        'carbs_g': round(carbs_g, 1),
        'calculado': calculado,
        'perfil_seleccionado': perfil_seleccionado,
    }
    return render(request, 'catalogo/nutricalculadora.html', context)