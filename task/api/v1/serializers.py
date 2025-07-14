from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('content', 'is_complete', 'created_at', 'updated_at')
        read_only_fields = ('is_complete', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
