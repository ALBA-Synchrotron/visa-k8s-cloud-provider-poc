from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from cloud_provider.models import Instance, ProposalAccount
from cloud_provider.serializers.security_group import SecurityGroupSerializer
from cloud_provider.services.flavour import FlavourService
from cloud_provider.services.image import ImageService
from cloud_provider.services.security_group import SecurityGroupService
from cloud_provider.utils.kubernetes.kubernetes_client import KubernetesClient
from mis_template.utils.models import TemplateModel


class InstanceSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(read_only=True)
    flavourId = serializers.CharField(source="flavour_id")
    imageId = serializers.CharField(source="image_id")
    createdAt = serializers.CharField(source="created_at")
    securityGroups = SecurityGroupSerializer(many=True, read_only=True, default=[], source="security_groups.all")
    state = serializers.SerializerMethodField(read_only=True)
    fault = serializers.SerializerMethodField(read_only=True)

    def get_address(self, instance) -> str or None:
        if instance.active and not instance.deleted_at:
            if instance.address:
                return instance.address
            return KubernetesClient.get_visa_instance_ip(instance.deployment_name)
        return None

    def get_state(self, instance) -> str:
        if instance.deleted_at:
            return "DELETED"
        state: str = KubernetesClient.get_visa_instance_state(instance.deployment_name)
        return state

    def get_fault(self, instance) -> dict:
        if not instance.active and instance.deleted_at:
            return {"message": "", "code": 0, "details": "",
                    "createdAt": instance.created_at.isoformat()}
        return KubernetesClient.get_visa_instance_fault(instance.deployment_name)

    def to_representation(self, instance) -> dict:
        ret: dict = super(InstanceSerializer, self).to_representation(instance)
        ret["id"] = str(instance.id)
        ret["createdAt"] = instance.created_at.isoformat()
        return ret

    class Meta:
        model: TemplateModel = Instance
        fields: list = ["id", "name", "state", "flavourId", "imageId", "createdAt", "address", "securityGroups",
                        "fault"]


class InstanceAddressSerializer(serializers.Serializer):
    ip = serializers.CharField(source="address", read_only=True)

    def to_representation(self, instance) -> dict:
        ret: dict = super(InstanceAddressSerializer, self).to_representation(instance)
        ret["id"], ret["ip"] = str(instance.address), str(instance.address)
        return ret

    class Meta:
        model: TemplateModel = Instance
        fields: list = ["id", "ip"]


class InstanceIdentifierSerializer(serializers.Serializer):

    def to_representation(self, instance) -> dict:
        ret: dict = super(InstanceIdentifierSerializer, self).to_representation(instance)
        ret["id"] = str(instance.id)
        return ret

    class Meta:
        model: TemplateModel = Instance
        fields: list = ["id"]


class InstanceMetadataSerializer(serializers.Serializer):
    owner = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    id = serializers.CharField(required=True)
    pamPublicKey = serializers.CharField(required=True)


class InstanceCreationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    imageId = serializers.CharField(required=True)
    flavourId = serializers.CharField(required=True)
    securityGroups = serializers.ListField(child=serializers.CharField(required=True))
    metadata = InstanceMetadataSerializer()
    bootCommand = serializers.CharField(allow_blank=True, default="")

    def validate(self, attrs) -> dict:
        try:
            _ = FlavourService().get_by_pk(attrs["flavourId"])
            _ = ImageService().get_by_pk(attrs["imageId"])
            for i in attrs["securityGroups"]:
                try:
                    _ = SecurityGroupService().get_by_field("name", i)
                except ObjectDoesNotExist:
                    if i.startswith("u"):
                        try:
                            _ = ProposalAccount.objects.get(username=f"u{i}")
                        except ObjectDoesNotExist:
                            # Ignore case when the proposal account does not exist -- storage will just not be mounted.
                            pass
        except ObjectDoesNotExist as e:
            raise e
        return attrs
