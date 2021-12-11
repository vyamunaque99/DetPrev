from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Credenciales incorrectas'
            context = {'error_message': error_message}
            return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        if password != repeat_password:
            error_message = 'Las contraseñas no coinciden'
            context = {'error_message': error_message}
            return render(request, 'register.html', context)
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            success_message = 'Usuario creado exitosamente'
            context = {'success_message': success_message}
            return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='login/')
def main_view(request):
    return render(request, 'main.html')


