from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   # Rutas Públicas
    path('menu/<slug:restaurante_slug>/', views.menu_publico, name='menu_publico'),

    # Rutas de Autenticación
    path('registro/', views.registro, name='registro'),
    
    # Usamos las vistas que Django ya trae para login y logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Rutas Privadas (dentro del sistema)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # (Más adelante aquí irán las URLs para crear/editar/borrar platos)
]