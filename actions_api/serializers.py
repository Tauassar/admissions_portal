from rest_framework import serializers

from actions_api.models import UserActionList


class ActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActionList
        exclude = ['updated_at', 'created_at']
