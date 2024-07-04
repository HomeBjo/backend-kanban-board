from rest_framework import serializers
from tasks.models import Task, Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'value', 'status']

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'assign_to', 'category', 'created_at', 'author', 'subtasks']
        extra_kwargs = {
            'author': {'required': False} 
        }
        
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        request = self.context.get('request')
        validated_data['author'] = request.user
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
       

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.assign_to = validated_data.get('assign_to', instance.assign_to)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        
        return instance
