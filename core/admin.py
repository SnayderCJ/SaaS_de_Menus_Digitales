from django.contrib import admin
from .models import Restaurante, Categoria, Plato

# Una forma más avanzada de registrar para mejorar la visualización
@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dueño', 'slug', 'activo') # Campos a mostrar en la lista
    search_fields = ('nombre', 'dueño__username') # Añade una barra de búsqueda
    list_filter = ('activo',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'restaurante')
    list_filter = ('restaurante__nombre',)

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible')
    list_filter = ('disponible', 'categoria__restaurante__nombre')
    search_fields = ('nombre',)