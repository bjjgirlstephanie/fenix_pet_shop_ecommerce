from django import forms

ESPECIE_CHOICES = [
    ('perro', 'Perro'),
    ('gato', 'Gato'),
]

ESTADO_CHOICES = [
    ('adulto_esterilizado', 'Adulto esterilizado'),
    ('adulto_entero', 'Adulto sin esterilizar'),
    ('sobrepeso', 'Propenso al sobrepeso / Perder peso'),
    ('cachorro', 'Cachorro / En crecimiento'),
    ('senior', 'Senior / Edad avanzada'),
]

class NutriCalculadoraForm(forms.Form):
    especie = forms.ChoiceField(choices=ESPECIE_CHOICES, label="Especie", widget=forms.Select(attrs={'class': 'form-select'}))
    peso_kg = forms.FloatField(label="Peso (en kg)", min_value=0.5, max_value=100.0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 8.5'}))
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label="Etapa / Condición", widget=forms.Select(attrs={'class': 'form-select'}))
    kcal_por_kg = forms.FloatField(
        label="Calorías del alimento (kcal/kg)",
        initial=3500.0,
        help_text="Por defecto se calcula con un promedio de 3500 kcal/kg si no conoces el dato del empaque.",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )