from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'lugares', views.LugarViewSet)
router.register(r'eventos', views.EventoViewSet) 
router.register(r'asientos', views.AsientoViewSet)
router.register(r'entradas', views.EntradaViewSet)
router.register(r'pagos', views.PagoViewSet)
router.register(r'categorias', views.CategoriaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/eventos/destacados/', views.EventoDestacadoListView.as_view(), name='eventos-destacados'),
    path('api/eventos/promocionados/', views.EventoPromocionadoListView.as_view(), name='eventos-promocionados'),
    path('api/', include(router.urls)),
]

# --- CONFIGURACIÓN PARA SERVIR IMÁGENES EN DESARROLLO ---

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# By: Edson DO