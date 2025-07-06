from django.contrib import admin
from django.urls import path, include
# --- Imports para servir archivos de medios en desarrollo ---
from django.conf import settings
from django.conf.urls.static import static
# --- Imports de la app y del router ---
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
    # URL para el panel de administrador de Django
    path('admin/', admin.site.urls),
    # URL para el login. Usamos tu CustomAuthToken para obtener el token.
    path('api/login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    # --- ¡NUEVAS URLS PARA EL FRONTEND! ---
    path('api/eventos/destacados/', views.EventoDestacadoListView.as_view(), name='eventos-destacados'),
    path('api/eventos/promocionados/', views.EventoPromocionadoListView.as_view(), name='eventos-promocionados'),
    
    #path('api/categorias/', views.CategoriaListView.as_view(), name='categorias-lista'),

    # Estas serán para operaciones más complejas (ej: /api/eventos/1/, /api/usuarios/3/)
    path('api/', include(router.urls)),
    path('api/token-auth/', views.CustomAuthToken.as_view(),name='token-auth'),
]

# --- CONFIGURACIÓN PARA SERVIR IMÁGENES EN DESARROLLO ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# By: Edson DO