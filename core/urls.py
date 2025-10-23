from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, menu_publico, registro, dashboard, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .forms import CustomAuthenticationForm

urlpatterns = [
    # Rutas Públicas
    path('', home, name='home'),
    path('menu/<slug:restaurante_slug>/', menu_publico, name='menu_publico'),

    # Rutas de Autenticación
    path('registro/',registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(
        template_name='pages/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Rutas Privadas
    path('dashboard/', dashboard, name='dashboard'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria_eliminar'),
]