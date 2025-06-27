from rest_framework import serializers
from . import models

# --------------------------
# Rol
# --------------------------

class RolSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = '__all__'

# --------------------------
# Usuario
# --------------------------

class UsuarioSerializador(serializers.ModelSerializer):
    Rol = RolSerializador(read_only=True)
    idRol = serializers.PrimaryKeyRelatedField(
        queryset=models.Rol.objects.all(),
        source='Rol',
        write_only=True
    )

    class Meta:
        model = models.Usuario
        fields = ['idUsuario', 'username', 'email', 'fecha_registro', 'Rol', 'idRol']

# --------------------------
# Lugar
# --------------------------

class LugarSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Lugar
        fields = '__all__'

# --------------------------
# Evento
# --------------------------

class EventoSerializador(serializers.ModelSerializer):
    Lugar = LugarSerializador(read_only=True)
    idLugar = serializers.PrimaryKeyRelatedField(
        queryset=models.Lugar.objects.all(), source='Lugar', write_only=True
    )

    CreadoPor = UsuarioSerializador(read_only=True)
    idCreadoPor = serializers.PrimaryKeyRelatedField(
        queryset=models.Usuario.objects.all(), source='CreadoPor', write_only=True
    )

    class Meta:
        model = models.Evento
        fields = [
            'idEvento', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'Lugar', 'idLugar', 'CreadoPor', 'idCreadoPor', 'imagen'
        ]

# --------------------------
# Asiento
# --------------------------

class AsientoSerializador(serializers.ModelSerializer):
    Lugar = LugarSerializador(read_only=True)
    idLugar = serializers.PrimaryKeyRelatedField(
        queryset=models.Lugar.objects.all(), source='Lugar', write_only=True
    )

    class Meta:
        model = models.Asiento
        fields = ['idAsiento', 'Fila', 'NumeroUnicoAsiento', 'TipoAsiento', 'disponible', 'Lugar', 'idLugar']

# --------------------------
# Entrada
# --------------------------

class EntradaSerializador(serializers.ModelSerializer):
    Usuario = UsuarioSerializador(read_only=True)
    idUsuario = serializers.PrimaryKeyRelatedField(
        queryset=models.Usuario.objects.all(), source='Usuario', write_only=True
    )

    Evento = EventoSerializador(read_only=True)
    idEvento = serializers.PrimaryKeyRelatedField(
        queryset=models.Evento.objects.all(), source='Evento', write_only=True
    )

    Asiento = AsientoSerializador(read_only=True)
    idAsiento = serializers.PrimaryKeyRelatedField(
        queryset=models.Asiento.objects.all(), source='Asiento', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = models.Entrada
        fields = [
            'idEntrada', 'Usuario', 'idUsuario', 'Evento', 'idEvento',
            'Asiento', 'idAsiento', 'CodigoQr', 'FechaDeCompra', 'estado'
        ]
        read_only_fields = ['CodigoQr', 'FechaDeCompra', 'estado']

# --------------------------
# Pago
# --------------------------

class PagoSerializador(serializers.ModelSerializer):
    Entrada = EntradaSerializador(read_only=True)
    idEntrada = serializers.PrimaryKeyRelatedField(
        queryset=models.Entrada.objects.all(), source='Entrada', write_only=True
    )

    class Meta:
        model = models.Pago
        fields = ['idPago', 'Entrada', 'idEntrada', 'metodo', 'estado', 'fecha', 'monto']
        read_only_fields = ['fecha']

# By: Edson DO
