from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api import views

# Imagenes
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'roles', views.RolViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'lugares', views.LugarViewSet)
router.register(r'eventos', views.EventoViewSet)
router.register(r'asientos', views.AsientoViewSet)
router.register(r'entradas', views.EntradaViewSet)
router.register(r'pagos', views.PagoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('api/token-auth/', views.CustomAuthToken.as_view(),name='token-auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# By: Edson DO