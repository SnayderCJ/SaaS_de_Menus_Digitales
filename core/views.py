from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Restaurante
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Categoria
from django.contrib.auth import login 

# --- Vistas Públicas ---

def landing_page(request):
    """ Muestra la página de inicio/ventas de tu SaaS. """
    return render(request, 'landing_page.html')


def menu_publico(request, restaurante_slug):
    """ Muestra el menú de un restaurante específico. """
    restaurante = get_object_or_404(Restaurante, slug=restaurante_slug)
    context = {'restaurante': restaurante}
    return render(request, 'menu_publico.html', context)

# --- Vistas de Autenticación ---

def registro(request):
    """ Maneja el registro y el inicio de sesión automático. """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario en la base de datos
            user = form.save()
            
            # Crea y vincula el perfil del restaurante
            Restaurante.objects.create(
                dueño=user, 
                nombre=f"Restaurante de {user.username}", 
                slug=f"{user.username}-menu"
            )
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'layout/registro.html', {'form': form})

# --- Vistas Privadas ---

@login_required
def dashboard(request):
    """ Muestra el panel de control al dueño del restaurante. """
    # Busca el restaurante del usuario logueado
    try:
        restaurante = request.user.restaurante
    except Restaurante.DoesNotExist:
        # Esto puede pasar si algo falla en el registro. Es una salvaguarda.
        return render(request, 'error.html', {'message': 'No tienes un restaurante asociado.'})

    context = {'restaurante': restaurante}
    return render(request, 'dashboard.html', context)

class CategoriaCreateView(CreateView):
    model = Categoria
    fields = ['nombre'] # Solo pediremos el nombre de la categoría
    template_name = 'categoria_form.html'
    success_url = reverse_lazy('dashboard') # Redirige al dashboard si es exitoso

    def form_valid(self, form):
        # Antes de guardar el formulario, asignamos el restaurante del usuario actual.
        # Esta es la lógica multi-inquilino.
        form.instance.restaurante = self.request.user.restaurante
        return super().form_valid(form)