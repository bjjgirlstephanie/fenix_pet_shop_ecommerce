# tienda/forms.py
# tienda/forms.py

from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group


class RegistroForm(SignupForm):
    nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"})
    )
    apellido = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"}),
        required=False
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("nombre", "")
        user.last_name = self.cleaned_data.get("apellido", "")
        user.is_staff = False       # no acceso al admin
        user.is_superuser = False   # no superusuario
        user.save()

        # asignar al grupo "Clientes"
        clientes_group, created = Group.objects.get_or_create(name="Clientes")
        user.groups.add(clientes_group)

        return user


class CustomLoginForm(LoginForm):
    login = forms.CharField(
        label="Usuario o Email",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Tu usuario o correo"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Tu contraseña"
        })
    )
