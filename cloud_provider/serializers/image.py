from rest_framework import serializers

from cloud_provider.models import Image
from mis_template.utils.models import TemplateModel


class ImageSerializer(serializers.ModelSerializer):
    createdAt: str = serializers.DateTimeField(source="created_at", read_only=True)

    def to_representation(self, instance) -> dict:
        ret: dict = super(ImageSerializer, self).to_representation(instance)
        ret["id"] = str(instance.pk)
        return ret

    class Meta:
        model: TemplateModel = Image
        fields: list = ["id", "name", "size", "createdAt"]
        depth: int = 1
