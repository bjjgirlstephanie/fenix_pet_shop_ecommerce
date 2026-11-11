# carrito/forms.py
from django import forms


class CarritoAddProductoForm(forms.Form):
    """
    Formulario simple para gestionar la cantidad de productos en el carrito.
    """
    # Campo para la cantidad (limitado a 99 unidades por operación)
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm text-center w-auto',
            'style': 'max-width: 80px;',
            'placeholder': 'Qty'
        })
    )

    # Campo oculto para diferenciar si se está añadiendo o actualizando la cantidad
    actualizar = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )