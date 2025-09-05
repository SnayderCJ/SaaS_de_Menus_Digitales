from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Clases de Tailwind que queremos aplicar a cada campo
        field_classes = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        
        # Iteramos sobre cada campo del formulario para añadirle las clases
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': field_classes})
            
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Clases de Tailwind
        field_classes = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        
        # Personalizamos el campo de usuario
        self.fields['username'].widget.attrs.update({
            'class': field_classes,
            'placeholder': 'Nombre de usuario'
        })
        
        # Personalizamos el campo de contraseña
        self.fields['password'].widget.attrs.update({
            'class': field_classes,
            'placeholder': '•••••••••'
        })