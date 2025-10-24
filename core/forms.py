from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Restaurante, Categoria, Plato

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_classes = (
            "w-full px-4 py-3 border border-gray-300 rounded-lg "
            "focus:outline-none focus:ring-2 focus:ring-purple-400 transition "
            "text-gray-700 bg-white"
        )
        for fieldname, field in self.fields.items():
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{classes} {field_classes}'

        self.fields['username'].widget.attrs.setdefault('placeholder', 'Nombre de usuario')
        self.fields['password1'].widget.attrs.setdefault('placeholder', 'Contraseña')
        self.fields['password2'].widget.attrs.setdefault('placeholder', 'Repite la contraseña')

        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_classes = (
            "w-full px-4 py-3 border border-gray-300 rounded-lg "
            "focus:outline-none focus:ring-2 focus:ring-purple-400 transition "
            "text-gray-700 bg-white"
        )
        self.fields['username'].widget.attrs['class'] = field_classes
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'

        self.fields['password'].widget.attrs['class'] = field_classes
        self.fields['password'].widget.attrs['placeholder'] = '•••••••••'
        
class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nombre', 'logo']  
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition text-gray-700 bg-white',
                'placeholder': 'Nombre del restaurante',
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'w-full bg-white px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition',
            }),
        }
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg '
                         'focus:outline-none focus:ring-2 focus:ring-purple-400 transition '
                         'text-gray-700 bg-white',
                'placeholder': 'Bebidas, Postres, Entradas...',
            }),
        }

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition text-gray-700 bg-white',
                'placeholder': 'Nombre del plato',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition text-gray-700 bg-white',
                'rows': 3,
                'placeholder': 'Descripción breve del plato...',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition text-gray-700 bg-white',
                'placeholder': 'Precio',
                'min': '0',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-purple-500 focus:ring-2 focus:ring-purple-400',
            }),
        }
