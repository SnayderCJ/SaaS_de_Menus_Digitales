from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import Restaurante
from django.contrib.auth.decorators import login_required

def menu_publico(request, restaurante_slug):
    # Busca el restaurante por su 'slug' o muestra un error 404 si no existe.
    # Esta es la forma segura de hacerlo.
    restaurante = get_object_or_404(Restaurante, slug=restaurante_slug)
    
    # Prepara el contexto para pasarlo a la plantilla
    context = {
        'restaurante': restaurante
    }
    return render(request, 'core/menu_publico.html', context)
 
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ¡Importante! Después de crear el usuario,
            # creamos su perfil de Restaurante vacío.
            # Aquí le pides más datos o creas uno por defecto.
            Restaurante.objects.create(dueño=user, nombre="Nombre de tu Restaurante", slug=f"tu-slug-{user.username}")
            # Puedes redirigirlo al login o a su dashboard
            return redirect('login') 
    else:
        form = UserCreationForm()
    
    return render(request, 'layout/registro.html', {'form': form})
 
@login_required
def dashboard(request):
    # Obtenemos el restaurante asociado al usuario que ha iniciado sesión
    try:
        restaurante = request.user.restaurante
    except Restaurante.DoesNotExist:
        # Manejar el caso de que un usuario no tenga restaurante (raro pero posible)
        return render(request, 'core/error.html', {'message': 'No tienes un restaurante asociado.'})

    context = {
        'restaurante': restaurante
    }
    return render(request, 'core/dashboard.html', context)