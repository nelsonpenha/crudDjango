from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from producto.forms import ProductoForm
from producto.models import Producto

from django.contrib.auth.models import User


# Create your views here.
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'actualizar_producto.html', {'form': form})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def crear_usuario(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],  password =request.POST['password1'])
                login(request, user)
                return redirect('lista_productos')
            except IntegrityError:
                return render(request, 'crear_usuario.html', {"form": UserCreationForm, "error": "El usuario ya existe"})
        return render(request, 'crear_usuario.html', {'form': UserCreationForm, "error": "Las contraseñas no coinciden"})
    return render(request, 'crear_usuario.html', {'form': UserCreationForm})

def iniciar_sesion(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('lista_productos')
        return render(request, 'iniciar_sesion.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrecto"})
    return render(request, 'iniciar_sesion.html', {"form": AuthenticationForm})