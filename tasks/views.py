from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from tasks.models import Task, Subtask
from tasks.serializers import TaskSerializer , SubtaskSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class AllTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                task = Task.objects.get(pk=pk, author=request.user)
                serializer = TaskSerializer(task)
            except Task.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            todos = Task.objects.filter(author=request.user)
            serializer = TaskSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        try:
            todo = Task.objects.get(pk=pk, author=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Todo item not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(todo, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            todo = Task.objects.get(pk=pk, author=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Todo item not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SubtaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, task_id, pk):
        try:
            return Subtask.objects.get(task_id=task_id, pk=pk)
        except Subtask.DoesNotExist:
            return None
        
    def get(self, request, task_id, pk, format=None):
        subtask = self.get_object(task_id, pk)
        if subtask is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubtaskSerializer(subtask)
        return Response(serializer.data)
    
    def patch(self, request, task_id, pk, format=None):
        subtask = self.get_object(task_id, pk)
        if subtask is None:
            return Response({"error": "Subtask not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)
        
        # Extrahiere die spezifischen Subtask-Daten
        subtask_data = None
        for data in request.data.get('subtasks', []):
            if data.get('id') == pk:
                subtask_data = data
                break
        
        if not subtask_data:
            return Response({"error": "Subtask data not found in request."}, status=status.HTTP_400_BAD_REQUEST)
        
        print("Received data for patch:", subtask_data)  # Debugging-Statement

        serializer = SubtaskSerializer(subtask, data=subtask_data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("Serializer errors:", serializer.errors)  # Debugging-Statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, task_id, format=None):
        try:
            task = Task.objects.get(pk=task_id, author=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to add a subtask to it."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id, pk, format=None):
        try:
           subtask = Subtask.objects.get(pk=pk, task_id=task_id)
        except Subtask.DoesNotExist:
          return Response({"error": "Subtask not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)
    
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

