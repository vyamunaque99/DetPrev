from django.http.response import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import uploadDatasetForm
from .models import Dataset
import pandas as pd
import json
import os
import pm4py

# Validacion de usuario logeado
def user_is_not_logged_in(user):
    return not user.is_authenticated

# Vista de login
@user_passes_test(user_is_not_logged_in, '/')
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
            # Se crea un usuario a traves de la clase por defecto
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


@login_required
def dataset_generation_view(request):
    if request.method == 'GET':
        form = uploadDatasetForm()
        context = {'form': form}
        return render(request, 'dataset_generation/dataset_generation_upload.html', context)
    else:
        print(request.POST['step'])
        if request.POST['step'] == '0':
            form = uploadDatasetForm(request.POST, request.FILES)
            if form.is_valid():
                dataset_table = dataset_handler(request.FILES['file'],request.POST['separator'])
                dataset_table_full = dataset_table[0]
                dataset_table_html = dataset_table[1]
                context = {
                    'dataset_table_html': dataset_table_html, 'form': form}
                # Almacenamiento de objetos en sesion
                request.session['dataset_table_full'] = dataset_table_full
                request.session['dataset_table_html'] = dataset_table_html
                request.session['indexes'] = {}
            return render(request, 'dataset_generation/dataset_generation_step_1.html', context)
        elif request.POST['step'] == '1':
            id_index = request.POST['id_index']
            dataset_table_html = request.session.get('dataset_table_html')
            context = {'dataset_table_html': dataset_table_html}
            # Se agrega el indice al diccionario de indices
            indexes = request.session.get('indexes')
            indexes['id_index'] = int(id_index)
            request.session['indexes'] = indexes
            return render(request, 'dataset_generation/dataset_generation_step_2.html', context)
        elif request.POST['step'] == '2':
            activity_index = request.POST['activity_index']
            dataset_table_html = request.session.get('dataset_table_html')
            context = {'dataset_table_html': dataset_table_html}
            # Se agrega el indice al diccionario de indices
            indexes = request.session.get('indexes')
            indexes['activity_index'] = int(activity_index)
            request.session['indexes'] = indexes
            print(indexes)
            return render(request, 'dataset_generation/dataset_generation_step_3.html', context)
        elif request.POST['step'] == '3':
            dataset_name = request.POST['dataset_name']
            #Validacion de formulario
            timestamp_index = request.POST['timestamp_index']
            if dataset_name=='':
                error_message='El dataset debe contener un nombre'
                dataset_table_html = request.session.get('dataset_table_html')
                context = {'dataset_table_html': dataset_table_html,'error_message':error_message}
                return render(request, 'dataset_generation/dataset_generation_step_3.html', context)
            elif ' ' in dataset_name:
                error_message='El nombre del dataset no debe contener espacios'
                dataset_table_html = request.session.get('dataset_table_html')
                context = {'dataset_table_html': dataset_table_html,'error_message':error_message}
                return render(request, 'dataset_generation/dataset_generation_step_3.html', context) 
            dataset_table_full = request.session.get('dataset_table_full')
            context = {'dataset_table_full': dataset_table_full}
            # Se agrega el indice al diccionario de indices
            indexes = request.session.get('indexes')
            indexes['timestamp_index'] = int(timestamp_index)
            request.session['indexes'] = indexes
            # Procesamiento de DataFrame
            print(type(indexes['id_index']))
            processed_dataframe = pd.DataFrame.from_dict(dataset_table_full)
            processed_dataframe = processed_dataframe.iloc[:, [
                indexes['id_index'], indexes['activity_index'], indexes['timestamp_index']]]
            # Almacenamiento de DataFrame
            if not os.path.exists(os.path.join(os.getcwd(),'main','assets',request.user.get_username(),dataset_name)):
                os.makedirs(os.path.join(os.getcwd(),'main','assets',request.user.get_username(),dataset_name))       
            processed_dataframe.to_csv('main/assets/{}/{}/dataset.csv'.format(request.user.get_username(),dataset_name), index=False)
            dataset=Dataset.objects.create(name=dataset_name,user=request.user)
            dataset.save()
            return render(request, 'dataset_generation/dataset_success.html', context)
        else:
            return redirect('/')


def dataset_handler(file,separator):
    # Procesamiento dataset completo
    dataset_1 = pd.read_csv(file,sep=separator)
    json_recods_1 = dataset_1.to_json(orient='records')
    data_1 = []
    data_1 = json.loads(json_recods_1)
    # Procesamiento dataset para HTML
    dataset_2 = dataset_1.head()
    json_recods_2 = dataset_2.to_json(orient='records')
    data_2 = []
    data_2 = json.loads(json_recods_2)
    return [data_1, data_2]

@login_required
def process_generation_view(request):
    datasets=Dataset.objects.all().filter(user=request.user)
    context={'datasets':datasets}
    return render(request, 'process_generation.html', context)

@login_required
def process_generation_detail(request,username,dataset_name):
    event_log=pd.read_csv('main/assets/{}/{}/dataset.csv'.format(username,dataset_name))
    event_log=pm4py.format_dataframe(event_log,case_id='case_id',activity_key='activity',timestamp_key='timestamp')
    process_tree=pm4py.discover_tree_inductive(event_log)
    bpmn_model=pm4py.convert_to_bpmn(process_tree)
    pm4py.save_vis_bpmn(bpmn_model,'main/assets/{}/{}/process.png'.format(username,dataset_name))
    img=open('main/assets/{}/{}/process.png'.format(username,dataset_name),'rb')
    return FileResponse(img)