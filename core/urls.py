from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, menu_publico, registro, dashboard, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, PlatoCreateView, CustomLoginView, PlatoUpdateView, PlatoDeleteView

urlpatterns = [
    # Rutas Públicas
    path('', home, name='home'),
    path('menu/<slug:restaurante_slug>/', menu_publico, name='menu_publico'),

    # Rutas de Autenticación
    path('registro/',registro, name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Rutas Privadas
    path('dashboard/', dashboard, name='dashboard'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    
    # PLato 
    path('categoria/<int:categoria_id>/platos/nuevo/', PlatoCreateView.as_view(), name='plato_crear'),
    path('platos/<int:pk>/editar/', PlatoUpdateView.as_view(), name='plato_editar'),
    path('platos/<int:pk>/eliminar/', PlatoDeleteView.as_view(), name='plato_eliminar'),    
]