from django.urls import path
from .views import get_demo_data, demo_table_view, login_view, task_edit_view, update_task, delete_task, create_task_view, create_task_post # Asegúrate de importar la vista de edición
from . import views

urlpatterns = [
    path('demo/', get_demo_data, name='get_demo_data'),
    path('demo/table/', demo_table_view, name='demo_table_view'),  # Cambia a una URL más específica si es necesario
    path('login/', login_view, name='login'),
    path('task/edit/<int:task_id>/', task_edit_view, name='task_edit'),  
    path('api/task/update/<int:task_id>/', update_task, name='update_task'),
    path('api/task/delete/<int:task_id>/', delete_task, name='delete_task'), 
    path('task/create/', create_task_view, name='create_task'), 
    path('api/task/create_task_post/', create_task_post, name='create_task_post'),
]
