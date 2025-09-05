from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CategoriaCreateView
from .forms import CustomAuthenticationForm
from . import views

urlpatterns = [
    # Rutas Públicas
    path('', views.landing_page, name='landing_page'),
    path('menu/<slug:restaurante_slug>/', views.menu_publico, name='menu_publico'),

    # Rutas de Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(
        template_name='layout/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    
    # Rutas Privadas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/categoria/nueva/', CategoriaCreateView.as_view(), name='categoria_crear'),
]