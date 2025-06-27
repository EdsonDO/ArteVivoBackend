from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from . import models, serializers

# --------------------------
# Vista de Rol
# --------------------------

class RolViewSet(viewsets.ModelViewSet):
    queryset = models.Rol.objects.all()
    serializer_class = serializers.RolSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Usuario
# --------------------------

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Lugar
# --------------------------

class LugarViewSet(viewsets.ModelViewSet):
    queryset = models.Lugar.objects.all()
    serializer_class = serializers.LugarSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Evento
# --------------------------

class EventoViewSet(viewsets.ModelViewSet):
    queryset = models.Evento.objects.all()
    serializer_class = serializers.EventoSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Asiento
# --------------------------

class AsientoViewSet(viewsets.ModelViewSet):
    queryset = models.Asiento.objects.all()
    serializer_class = serializers.AsientoSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Entrada
# --------------------------

class EntradaViewSet(viewsets.ModelViewSet):
    queryset = models.Entrada.objects.all()
    serializer_class = serializers.EntradaSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Vista de Pago
# --------------------------

class PagoViewSet(viewsets.ModelViewSet):
    queryset = models.Pago.objects.all()
    serializer_class = serializers.PagoSerializador
    permission_classes = [permissions.IsAuthenticated]

# --------------------------
# Token personalizado (Login API)
# --------------------------

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