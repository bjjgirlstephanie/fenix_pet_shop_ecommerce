# tienda/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Compra

@receiver(post_save, sender=Compra)
def enviar_notificacion_compra(sender, instance, created, **kwargs):
    if created:
        asunto = "Nueva compra realizada"
        mensaje = (
            f"El cliente {instance.cliente.username} ha comprado "
            f"{instance.cantidad} unidad(es) de {instance.producto}."
        )
        destinatario = ["tu_correo@gmail.com"]  # tu correo de administradora

        send_mail(asunto, mensaje, None, destinatario)
