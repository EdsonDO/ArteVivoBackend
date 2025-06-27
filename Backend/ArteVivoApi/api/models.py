from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# --------------------------
# Gestión de Usuarios con Rol
# --------------------------

class Rol(models.Model):
    nombre = models.CharField(max_length=50)  # "cliente", "admin"

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Correo es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    idUsuario = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

# --------------------------
# Localizaciones genéricas
# --------------------------

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # estadio, teatro, colegio, etc.
    direccion = models.TextField()
    tiene_asientos = models.BooleanField(default=True)

# --------------------------
# Eventos
# --------------------------

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="eventos_creados")
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)

# --------------------------
# Asientos (opcional, según lugar)
# --------------------------

class Asiento(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    fila = models.CharField(max_length=5)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=30, default='General')  # VIP, Normal, etc.
    disponible = models.BooleanField(default=True)

# --------------------------
# Entradas (solo con pago confirmado)
# --------------------------

class Entrada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_qr = models.ImageField(upload_to='qr/', blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pagado')  # Solo "pagado" para evitar abuso

    def save(self, *args, **kwargs):
        if not self.codigo_qr:
            qr_data = f"{self.evento.nombre}-{self.usuario.username}-{uuid.uuid4()}"
            qr = qrcode.make(qr_data)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.codigo_qr.save(f"qr_{self.pk}.png", File(buffer), save=False)
        super().save(*args, **kwargs)

# --------------------------
# Pagos simulados
# --------------------------

class Pago(models.Model):
    entrada = models.OneToOneField(Entrada, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=30)  # "tarjeta", "yape", etc.
    estado = models.CharField(max_length=20, default='completado')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

# By: Edson DO