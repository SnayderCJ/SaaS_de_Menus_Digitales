from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# El perfil del dueño del restaurante
class Restaurante(models.Model):
    dueño = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Texto para la URL, ej: pizzeria-pepe. No usar espacios ni ñ.")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    activo = models.BooleanField(default=True) # Para activar/desactivar su menú

    def save(self, *args, **kwargs):
        # Crear un slug automáticamente si no existe
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            # Evitar duplicados
            while Restaurante.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre

# Las secciones del menú
class Categoria(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

# Cada plato del menú
class Plato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='platos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre