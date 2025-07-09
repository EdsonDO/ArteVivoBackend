from rest_framework import viewsets, permissions, generics

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models
from . import serializers


# --- VISTAS PARA LA PÁGINA DE INICIO (PÚBLICAS) ---

# Vista para devolver solo los eventos marcados como "destacados"
class EventoDestacadoListView(generics.ListAPIView):
    queryset = models.Evento.objects.filter(es_destacado=True).order_by('fecha_inicio')
    serializer_class = serializers.EventoSerializador
    permission_classes = [permissions.AllowAny]

# Vista para devolver solo los eventos marcados como "promocionados"
class EventoPromocionadoListView(generics.ListAPIView):
    queryset = models.Evento.objects.filter(es_promocionado=True).order_by('fecha_inicio')
    serializer_class = serializers.EventoSerializador
    permission_classes = [permissions.AllowAny]

# Vista para las categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Categoria.objects.all()
    serializer_class = serializers.CategoriaSerializador

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

class EventoViewSet(viewsets.ModelViewSet):
    queryset = models.Evento.objects.all()
    serializer_class = serializers.EventoSerializador
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

class LugarViewSet(viewsets.ModelViewSet):
    queryset = models.Lugar.objects.all()
    serializer_class = serializers.LugarSerializador
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AsientoViewSet(viewsets.ModelViewSet):
    queryset = models.Asiento.objects.all()
    serializer_class = serializers.AsientoSerializador
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializador
    permission_classes = [permissions.IsAuthenticated]

class EntradaViewSet(viewsets.ModelViewSet):
    queryset = models.Entrada.objects.all()
    serializer_class = serializers.EntradaSerializador
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return models.Entrada.objects.filter(usuario=self.request.user)

class PagoViewSet(viewsets.ModelViewSet):
    queryset = models.Pago.objects.all()
    serializer_class = serializers.PagoSerializador
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return models.Pago.objects.filter(entrada__usuario=self.request.user)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


# By: Edson DO