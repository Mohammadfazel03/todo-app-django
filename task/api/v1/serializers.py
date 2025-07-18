from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('content', 'is_complete', 'created_at', 'updated_at', 'id')
        read_only_fields = ('is_complete', 'created_at', 'updated_at', 'id')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskChangeStateSerializer(serializers.Serializer):
    is_complete = serializers.BooleanField(allow_null=False, required=True)