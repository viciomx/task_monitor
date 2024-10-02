from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_notification_email_task

class DemoTable(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demo_table'  # Asigna el nombre de la tabla aquí

    def __str__(self):
        return self.nombre
    

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Puedes usar un hash para almacenar contraseñas
    email = models.EmailField(max_length=255, unique=True)
    edad = models.IntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Cambia este nombre si lo deseas
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Cambia este nombre si lo deseas
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        db_table = 'usuarios'  # Asigna el nombre de la tabla aquí

    def __str__(self):
        return self.username


class TaskTable(models.Model):
    title = models.TextField()  # Cambiado a TextField
    email = models.TextField()  # Cambiado a TextField
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_table'  # Nombre de la tabla en la base de datos

    def __str__(self):
        return self.title
    

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user_email = models.EmailField()  # Correo del usuario

    def __str__(self):
        return self.title

# Señal para enviar un correo electrónico cuando se crea o actualiza una tarea
@receiver(post_save, sender=Task)
def notify_user(sender, instance, created, **kwargs):
    if created:
        subject = 'Nueva Tarea Creada'
        message = f'Tu tarea "{instance.title}" ha sido creada.'
    else:
        subject = 'Tarea Actualizada'
        message = f'Tu tarea "{instance.title}" ha sido actualizada.'

    send_notification_email_task(subject, message, 'tu_correo@gmail.com', [instance.user_email])