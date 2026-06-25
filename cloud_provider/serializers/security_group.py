from rest_framework import serializers

from cloud_provider.models import SecurityGroup
from mis_template.utils.models import TemplateModel


class SecurityGroupNameListSerializer(serializers.ListSerializer):
    def to_representation(self, data) -> list:
        return [item.name for item in data]

class SecurityGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model: TemplateModel = SecurityGroup
        fields: list = ["name"]
        depth: int = 1
        list_serializer_class = SecurityGroupNameListSerializer

