from rest_framework import serializers
from tasks.models import Task, Subtask
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

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
    assign_to = UserSerializer(many=True, read_only=True)
    assign_to_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'assign_to', 'assign_to_ids', 'category', 'created_at', 'author', 'subtasks']
        extra_kwargs = {
            'author': {'required': False}
        }

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assign_to_ids = validated_data.pop('assign_to_ids', [])
        request = self.context.get('request')
        validated_data['author'] = request.user
        task = Task.objects.create(**validated_data)
        task.assign_to.set(assign_to_ids)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assign_to_ids = validated_data.pop('assign_to_ids', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.category = validated_data.get('category', instance.category)
        instance.assign_to.set(assign_to_ids)
        instance.save()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                subtask = Subtask.objects.get(id=subtask_id, task=instance)
                subtask.value = subtask_data.get('value', subtask.value)
                subtask.status = subtask_data.get('status', subtask.status)
                subtask.save()
            else:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance
