# Notas



# Creacion de Formularios y estilos

Instala el paquete:

pip install django-bootstrap5

Agrega 'bootstrap5' a la lista de INSTALLED_APPS en el archivo settings.py:

INSTALLED_APPS = [
    ...,
    'bootstrap5',
    ...
]

Usa el formulario de Bootstrap en tu plantilla con {% load bootstrap5 %}:

    {% load bootstrap5 %}

    <form method="post">
        {% csrf_token %}
        {% bootstrap_form form %}
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

Esto te permitirá integrar Bootstrap de manera automática a los formularios y otros elementos de tu proyecto Django.
Resumen

Puedes usar Bootstrap en Django de manera rápida a través de un CDN, descargándolo localmente en tus archivos estáticos, o usando un paquete Django especializado como django-bootstrap5 para una integración más fluida con formularios.

¿Hay algún aspecto en particular del uso de Bootstrap con Django que te interese más?
Dijiste:
me darias un ejemplo de cómo armar un formulario de registro y login, y de cómo crearlos en django, que tengo instalado en manjaro, con un proyecto, que ya tengo creado...??
ChatGPT dijo:
ChatGPT

¡Por supuesto! Aquí tienes un ejemplo completo de cómo puedes crear formularios de registro y login en Django, usando Bootstrap para los estilos.
Paso 1: Crear la app de autenticación

Si no tienes una app específica para manejar la autenticación (login y registro), puedes crearla con el siguiente comando:

python manage.py startapp accounts

Paso 2: Agregar la app a INSTALLED_APPS

Abre el archivo settings.py de tu proyecto y agrega la app accounts a la lista de INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    'accounts',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

Paso 3: Crear el modelo de usuario (si no usas el modelo por defecto)

Si necesitas un modelo de usuario personalizado (por ejemplo, agregar campos adicionales), puedes hacerlo extendiendo el modelo AbstractUser. Aquí tienes un ejemplo de un modelo básico:

# accounts/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Puedes agregar más campos si lo necesitas
    pass

Luego, debes indicarle a Django que use este modelo personalizado. En tu settings.py, agrega:

AUTH_USER_MODEL = 'accounts.CustomUser'

Si decides no personalizar el modelo de usuario, puedes usar el modelo de usuario por defecto de Django (User).
Paso 4: Crear formularios de registro y login
Formulario de Registro

Puedes crear un formulario para el registro de usuarios utilizando el formulario UserCreationForm de Django, o puedes crear uno personalizado.

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

Formulario de Login

Django ya tiene un formulario de login predeterminado, pero puedes crear un formulario personalizado si lo prefieres.

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

Paso 5: Crear vistas para registro y login

Ahora, creamos las vistas en el archivo views.py de la app accounts para manejar el registro y el login.
Vista de Registro

# accounts/views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' a la vista que quieras redirigir después del registro
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

Vista de Login

# accounts/views.py
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')  # Cambia 'home' a la vista que quieras redirigir después del login
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

Paso 6: Crear las plantillas

Ahora, crea las plantillas HTML para el formulario de registro y login.
Plantilla de registro (register.html)

<!-- accounts/templates/accounts/register.html -->
{% load bootstrap5 %}

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container">
    <h2>Registro</h2>
    <form method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <button type="submit" class="btn btn-primary">Registrarse</button>
    </form>
</div>

</body>
</html>

Plantilla de login (login.html)

<!-- accounts/templates/accounts/login.html -->
{% load bootstrap5 %}

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container">
    <h2>Iniciar Sesión</h2>
    <form method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <button type="submit" class="btn btn-primary">Iniciar sesión</button>
    </form>
</div>

</body>
</html>

Paso 7: Configurar las URLs

Ahora, necesitas configurar las URLs para que las vistas de login y registro estén accesibles. Abre o crea el archivo urls.py dentro de la app accounts y agrega las rutas correspondientes.

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]

Luego, agrega estas rutas en el archivo urls.py principal de tu proyecto (el que está en la raíz del proyecto):

# proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Otras rutas
]

Paso 8: Ejecutar el servidor y probar

Ahora puedes ejecutar el servidor:

python manage.py runserver

Ve a http://127.0.0.1:8000/accounts/register/ para el formulario de registro y http://127.0.0.1:8000/accounts/login/ para el formulario de login.

