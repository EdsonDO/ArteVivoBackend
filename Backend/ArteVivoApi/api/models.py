from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email: raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    idUsuario = models.AutoField(primary_key=True)
    fecha_registro = models.DateField(auto_now_add=True)
    objects = UsuarioManager()
    def __str__(self): return self.username

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    direccion = models.TextField()
    tiene_asientos = models.BooleanField(default=True)
    def __str__(self): return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    def __str__(self): return self.nombre

class Evento(models.Model):
    TIPO_ENTRADA_CHOICES = [('numerado', 'Asiento Numerado'), ('general', 'Entrada General')]
    tipo_entrada = models.CharField(max_length=10, choices=TIPO_ENTRADA_CHOICES, default='numerado')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="eventos_creados")
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    es_destacado = models.BooleanField(default=False, help_text="Marcar para el carrusel principal.")
    es_promocionado = models.BooleanField(default=False, help_text="Marcar para la sección inferior.")
    def __str__(self): return self.nombre

class Asiento(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    seccion = models.CharField(max_length=50, default='General')
    fila = models.CharField(max_length=5)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=30, default='General')
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    def __str__(self): return f"{self.lugar.nombre} - {self.seccion} - Fila {self.fila}, N° {self.numero}"

class Entrada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_qr = models.ImageField(upload_to='qr/', blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pagado')
    def save(self, *args, **kwargs):
        if not self.codigo_qr:
            qr_data = f"Evento:{self.evento.nombre}-Usuario:{self.usuario.username}-ID:{uuid.uuid4()}"
            qr_img = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            self.codigo_qr.save(f"qr_entrada_{self.pk}_{uuid.uuid4().hex[:6]}.png", File(buffer), save=False)
        super().save(*args, **kwargs)

class Pago(models.Model):
    entrada = models.OneToOneField(Entrada, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, default='completado')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
# By: Edson DO