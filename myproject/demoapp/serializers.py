from rest_framework import serializers
from .models import TaskTable  # Asegúrate de importar tu modelo

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTable
        fields = ['id', 'title', 'description', 'email']  # Asegúrate de incluir todos los campos que quieres actualizar
