from rest_framework import serializers

from cloud_provider.models import Flavour
from mis_template.utils.models import TemplateModel


class FlavourSerializer(serializers.ModelSerializer):

    def to_representation(self, instance) -> dict:
        ret: dict = super(FlavourSerializer, self).to_representation(instance)
        ret["id"] = str(instance.pk)
        return ret

    class Meta:
        model: TemplateModel = Flavour
        fields: str = "__all__"
        depth: int = 1
