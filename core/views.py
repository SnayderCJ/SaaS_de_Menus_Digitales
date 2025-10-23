from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm, RestauranteForm, CategoriaForm, PlatoForm, CustomAuthenticationForm
from .models import Restaurante, Categoria, Plato
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


# --- Vistas Públicas ---

def home(request):
    """ Muestra la página principal de tu SaaS """
    return render(request, 'pages/index.html')


def menu_publico(request, restaurante_slug):
    """ Muestra el menú público de un restaurante por slug """
    restaurante = get_object_or_404(Restaurante, slug=restaurante_slug)
    context = {'restaurante': restaurante}
    return render(request, 'components/menu_publico.html', context)


# --- Vistas de Autenticación ---

def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        rest_form = RestauranteForm(request.POST, request.FILES)

        if user_form.is_valid() and rest_form.is_valid():
            user = user_form.save()
            restaurante = rest_form.save(commit=False)
            restaurante.dueño = user
            restaurante.save()

            login(request, user)
            return redirect('dashboard')
    else:
        user_form = CustomUserCreationForm()
        rest_form = RestauranteForm()

    return render(request, 'pages/registro.html', {
        'form': user_form,
        'rest_form': rest_form
    })

class CustomLoginView(LoginView):
    template_name = 'pages/login.html'
    authentication_form = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario ya está logeado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
# --- Vistas Privadas ---

@login_required
def dashboard(request):
    """ Muestra el panel principal del restaurante """
    try:
        restaurante = request.user.restaurante
    except Restaurante.DoesNotExist:
        return render(request, 'pages/error.html', {
            'message': 'No tienes un restaurante asociado.'
        })

    context = {'restaurante': restaurante}
    return render(request, 'pages/dashboard.html', context)


# --- Categorías ---

class CategoriaCreateView(CreateView):
    """ Crear una nueva categoría dentro del restaurante del usuario actual """
    model = Categoria
    form_class = CategoriaForm             # <- Usamos el formulario personalizado
    template_name = 'pages/categoria_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.restaurante = self.request.user.restaurante
        return super().form_valid(form)
    
# --- Editar Categoría ---
class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'pages/categoria_form.html'  # reutilizamos el mismo formulario
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Solo permite editar categorías del restaurante del usuario actual
        return Categoria.objects.filter(restaurante=self.request.user.restaurante)


# --- Eliminar Categoría ---
class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'pages/categoria_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Solo permite eliminar categorías propias
        return Categoria.objects.filter(restaurante=self.request.user.restaurante)
    
class PlatoCreateView(CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'pages/plato_form.html'

    def get_success_url(self):
        categoria_id = self.kwargs['categoria_id']
        return reverse_lazy('dashboard')  # volver al dashboard tras guardar

    def form_valid(self, form):
        categoria = get_object_or_404(Categoria, id=self.kwargs['categoria_id'])
        form.instance.categoria = categoria
        return super().form_valid(form)