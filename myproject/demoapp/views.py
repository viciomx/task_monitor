from django.http import JsonResponse
from .models import TaskTable
from django.contrib.auth import  login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from .tasks import send_notification_email_task 

def demo_table_view(request):
    return render(request, 'demoapp/table_task.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, 'demoapp/login.html')

        if check_password(password, user.password):
            login(request, user)
            # Redirige a demo_table_view después de un inicio de sesión exitoso
            return redirect('demo_table_view')  # Asegúrate de que este nombre de vista esté en tu archivo urls.py
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'demoapp/login.html')

def create_task_view(request):
    return render(request, 'demoapp/create_task.html')


def task_edit_view(request, task_id):
    task = get_object_or_404(TaskTable, id=task_id)

    if request.method == 'POST':
        pass

    return render(request, 'demoapp/task_edit.html', {'task': task})



#apis
@api_view(['GET'])
def get_demo_data(request):
    datos = list(TaskTable.objects.values())
    return JsonResponse(datos, safe=False)

@api_view(['PUT'])
def update_task(request, task_id):
    task = get_object_or_404(TaskTable, id=task_id)
    serializer = TaskSerializer(task, data=request.data)

    if serializer.is_valid():
        serializer.save()
        subject = 'Tarea Creada Modificada'
        title = request.data.get('title')
        message = f'Tu tarea "{title}" ha sido modificada.'
        from_email = 'taskhost217@gmail.com'  # Cambia esto a tu correo
        recipient_list = [request.data.get('email')]  # Asegúrate de que el correo del usuario esté en la solicitud

        # Enviar la tarea de envío de correo electrónico de manera asíncrona
        send_notification_email_task(subject, message, from_email, recipient_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(TaskTable, id=task_id)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])  # Solo permite solicitudes POST
def create_task_post(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        print('aqui')
        # Preparar el correo electrónico
        subject = 'Nueva Tarea Creada'
        title = request.data.get('title')
        message = f'Tu tarea "{title}" ha sido creada.'
        from_email = 'taskhost217@gmail.com'  # Cambia esto a tu correo
        recipient_list = [request.data.get('email')]  # Asegúrate de que el correo del usuario esté en la solicitud

        # Enviar la tarea de envío de correo electrónico de manera asíncrona
        send_notification_email_task(subject, message, from_email, recipient_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)