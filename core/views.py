from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import (
    CustomUserCreationForm,
    RestauranteForm,
    CategoriaForm,
    PlatoForm,
    CustomAuthenticationForm,
    CustomUserProfileForm
)
from .models import Restaurante, Categoria, Plato

# --- Vistas Públicas ---

def home(request):
    return render(request, 'pages/index.html')

def handler404(request, exception):
    return render(request, 'pages/error.html', status=404)

def menu_publico(request, slug):
    restaurante = get_object_or_404(Restaurante, slug=slug)
    categorias = restaurante.categorias.prefetch_related('platos').all()
    return render(request, 'components/menu_publico.html', {
        'restaurante': restaurante,
        'categorias': categorias
    })

@login_required
def perfil(request):
    restaurante = request.user.restaurante
    user_form = CustomUserProfileForm(request.POST or None, instance=request.user)
    rest_form = RestauranteForm(request.POST or None, request.FILES or None, instance=restaurante)

    if request.method == 'POST':
        if user_form.is_valid() and rest_form.is_valid():
            user_form.save()
            rest_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
    return render(request, 'pages/perfil.html', {
        'user_form': user_form,
        'rest_form': rest_form,
        'restaurante': restaurante
    })

@login_required
def regenerar_qr(request):
    restaurante = request.user.restaurante
    restaurante.generar_qr()
    restaurante.save()
    messages.success(request, "Código QR regenerado correctamente.")
    return redirect('dashboard')

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
            messages.success(request, 'Registro completado con éxito. ¡Bienvenido a Menú.Pro!')
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
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

# --- Vistas Privadas (Dashboard) ---

@login_required
def dashboard(request):
    try:
        restaurante = request.user.restaurante
    except Restaurante.DoesNotExist:
        return render(request, 'pages/error.html', {
            'message': 'No tienes un restaurante asociado.'
        })
    categorias = restaurante.categorias.all().order_by('nombre')
    paginator = Paginator(categorias, 2)  # Cambia a 6 si quieres mostrar más 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'restaurante': restaurante, 'page_obj': page_obj}
    return render(request, 'pages/dashboard.html', context)

# --- Categorías ---

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'pages/categoria_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.restaurante = self.request.user.restaurante
        messages.success(self.request, 'Categoría creada correctamente.')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'pages/categoria_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.info(self.request, 'Categoría actualizada correctamente.')
        return super().form_valid(form)

    def get_queryset(self):
        return Categoria.objects.filter(restaurante=self.request.user.restaurante)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'pages/categoria_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.error(request, 'Categoría eliminada correctamente.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Categoria.objects.filter(restaurante=self.request.user.restaurante)

# --- Platos ---

class PlatoCreateView(LoginRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'pages/plato_form.html'

    def form_valid(self, form):
        categoria = get_object_or_404(
            Categoria,
            id=self.kwargs['categoria_id'],
            restaurante=self.request.user.restaurante
        )
        form.instance.categoria = categoria
        messages.success(self.request, 'Plato agregado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

class PlatoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'pages/plato_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.info(self.request, 'Plato editado correctamente.')
        return super().form_valid(form)

    def get_queryset(self):
        return Plato.objects.filter(categoria__restaurante=self.request.user.restaurante)

class PlatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Plato
    template_name = 'pages/plato_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.error(request, 'Plato eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Plato.objects.filter(categoria__restaurante=self.request.user.restaurante)
