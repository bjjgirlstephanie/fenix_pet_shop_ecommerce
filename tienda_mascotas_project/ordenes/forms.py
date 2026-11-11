from django import forms
from .models import Orden

class OrdenCreateForm(forms.ModelForm):
    """
    Formulario para la creación de una orden, basado en el modelo Orden.
    Excluye campos automáticos o de estado.
    """
    class Meta:
        model = Orden
        fields = [
            'nombre',
            'apellido',
            'email',
            'direccion',
            'codigo_postal',
            'ciudad',
            'metodo_pago' #se gestiona en la vista para asegurar que el valor coincida
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle, número y referencias'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cód. Postal'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
        }




