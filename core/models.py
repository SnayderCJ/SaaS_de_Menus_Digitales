from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO
import qrcode
from django.conf import settings

class Restaurante(models.Model):
    dueño = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Texto para la URL, ej: pizzeria-pepe. No usar espacios ni ñ.")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True, help_text="Breve descripción o eslogan del restaurante.")
    activo = models.BooleanField(default=True, help_text="Controla si el menú público está activo o no.")
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, help_text="Código QR del menú público.")

    def save(self, *args, **kwargs):
        # Crear un slug automáticamente si no existe
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            # Evitar duplicados
            while Restaurante.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

        # Generar el código QR si no existe
        if not self.qr_code:
            self.generar_qr()

    def generar_qr(self):
        """Genera automáticamente un código QR con la URL pública del restaurante."""
        url_menu = f"{settings.SITE_URL}/restaurante/{self.slug}/"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url_menu)
        qr.make(fit=True)
        img = qr.make_image(fill_color="purple", back_color="white")

        # Guardar imagen QR en memoria
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f"qr-{self.slug}.png"
        self.qr_code.save(file_name, File(buffer), save=False)
        buffer.close()
        super().save(update_fields=['qr_code'])

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
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    

    def __str__(self):
        return self.nombre