from rest_framework import serializers
from . import models

class CategoriaSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Categoria
        fields = ['id', 'nombre', 'imagen']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.imagen:
            request = self.context.get('request')
            representation['imagen'] = request.build_absolute_uri(instance.imagen.url)
        return representation

class LugarSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Lugar
        fields = '__all__'

class EventoSerializador(serializers.ModelSerializer):
    lugar = serializers.StringRelatedField(read_only=True)
    categoria = serializers.StringRelatedField(read_only=True)
    lugar_id = serializers.PrimaryKeyRelatedField(queryset=models.Lugar.objects.all(), source='lugar', write_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=models.Categoria.objects.all(), source='categoria', write_only=True, required=False)
    class Meta:
        model = models.Evento
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'tipo_entrada',
            'imagen', 'lugar', 'lugar_id', 'categoria', 'categoria_id',
            'es_destacado', 'es_promocionado'
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.imagen:
            request = self.context.get('request')
            representation['imagen'] = request.build_absolute_uri(instance.imagen.url)
        return representation

class AsientoSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Asiento
        fields = ['id', 'lugar', 'seccion', 'fila', 'numero', 'tipo', 'disponible', 'precio']

class UsuarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['idUsuario', 'username', 'email', 'fecha_registro']

class EntradaSerializador(serializers.ModelSerializer):
    usuario = UsuarioSerializador(read_only=True)
    evento = EventoSerializador(read_only=True)
    asiento = AsientoSerializador(read_only=True)
    class Meta:
        model = models.Entrada
        fields = ['id', 'usuario', 'evento', 'asiento', 'codigo_qr', 'fecha_compra', 'estado']
        read_only_fields = ['codigo_qr', 'fecha_compra', 'estado']

class PagoSerializador(serializers.ModelSerializer):
    class Meta:
        model = models.Pago
        fields = ['id', 'entrada', 'metodo', 'estado', 'fecha', 'monto']
        read_only_fields = ['fecha']
