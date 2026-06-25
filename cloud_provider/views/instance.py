# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from cloud_provider.labels.model import instance as labels
from cloud_provider.labels.model.instance import MSG_INSTANCE_DOES_NOT_EXIST, \
    MSG_STARTING_INSTANCE, MSG_INSTANCE_DELETED, MSG_REBOOTING_INSTANCE, MSG_SHUTTING_DOWN_INSTANCE, \
    MSG_ADDED_SECURITY_GROUP, MSG_SECURITY_GROUP_DOES_NOT_EXIST, MSG_SECURITY_GROUP_NOT_ASSIGNED_IN_INSTANCE, \
    MSG_REMOVED_SECURITY_GROUP, MSG_DELETING_INSTANCE, MSG_ERROR_STARTING_INSTANCE, MSG_ERROR_DELETING_INSTANCE, \
    MSG_ERROR_STOPPING_INSTANCE, MSG_ERROR_REBOOTING_INSTANCE, MSG_ERROR_CREATING_INSTANCE
from cloud_provider.models import Instance, ProposalAccount, SecurityGroup
from cloud_provider.serializers.instance import InstanceAddressSerializer, InstanceCreationSerializer, \
    InstanceSerializer, InstanceIdentifierSerializer
from cloud_provider.serializers.security_group import SecurityGroupSerializer
from cloud_provider.services.flavour import FlavourService
from cloud_provider.services.image import ImageService
from cloud_provider.services.instance import InstanceService
from cloud_provider.services.security_group import SecurityGroupService
from cloud_provider.utils.kubernetes.kubernetes_client import KubernetesClient
from cloud_provider.utils.quota import check_instance_quota

default_model_class = Instance
default_service = InstanceService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
default_permission_content_type_name = "instance"
security_groups_service = SecurityGroupService()


class InstanceAddressDetail(RetrieveAPIView):
    serializer_class = InstanceAddressSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None


class GeneralInstance(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request, *args, **kwargs):
        serializer_class = InstanceSerializer
        instances = default_service.get_all()[::-1]
        return Response(data=serializer_class(instances, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        r = check_instance_quota()
        if r:
            return r
        serializer_class = InstanceCreationSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        image = ImageService().get_by_pk(serializer.validated_data["imageId"])
        flavour = FlavourService().get_by_pk(serializer.validated_data["flavourId"])
        sec_groups = serializer.validated_data["securityGroups"]
        metadata = serializer.validated_data["metadata"]
        boot_command = serializer.validated_data["bootCommand"]
        instance = KubernetesClient.create_visa_instance(name=name, image=image, flavour=flavour,
                                                         sec_groups=sec_groups, metadata=metadata,
                                                         boot_command=boot_command)
        if not instance:
            return Response(data={"message": MSG_ERROR_CREATING_INSTANCE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"id": str(instance.id)}, status=status.HTTP_201_CREATED)


class InstanceIdentifierList(ListAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = InstanceIdentifierSerializer
    queryset = default_model_class.objects.all()


class DetailInstance(RetrieveAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = InstanceSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(data={"message": MSG_INSTANCE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        if instance.deleted_at:
            return Response(data={"message": MSG_INSTANCE_DELETED}, status=status.HTTP_400_BAD_REQUEST)
        ret = KubernetesClient.delete_visa_instance(instance)
        if not ret:
            return Response(data={"message": MSG_ERROR_DELETING_INSTANCE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"message": MSG_DELETING_INSTANCE}, status=status.HTTP_200_OK)


class StartInstance(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = InstanceSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def post(self, request, *args, **kwargs):
        r = check_instance_quota()
        if r:
            return r
        instance = self.get_object()
        if not instance:
            return Response(data={"message": MSG_INSTANCE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        if instance.deleted_at:
            return Response(data={"message": MSG_INSTANCE_DELETED}, status=status.HTTP_400_BAD_REQUEST)
        ret = KubernetesClient.start_visa_instance(instance)
        if not ret:
            return Response(data={"message": MSG_ERROR_STARTING_INSTANCE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"message": MSG_STARTING_INSTANCE}, status=status.HTTP_200_OK)


class RebootInstance(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = InstanceSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(data={"message": MSG_INSTANCE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        if instance.deleted_at:
            return Response(data={"message": MSG_INSTANCE_DELETED}, status=status.HTTP_400_BAD_REQUEST)
        ret = KubernetesClient.reboot_visa_instance(instance)
        if not ret:
            return Response(data={"message": MSG_ERROR_REBOOTING_INSTANCE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"message": MSG_REBOOTING_INSTANCE}, status=status.HTTP_200_OK)


class ShutdownInstance(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = InstanceSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(data={"message": MSG_INSTANCE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        if instance.deleted_at:
            return Response(data={"message": MSG_INSTANCE_DELETED}, status=status.HTTP_400_BAD_REQUEST)
        ret =  KubernetesClient.stop_visa_instance(instance)
        if not ret:
            return Response(data={"message": MSG_ERROR_STOPPING_INSTANCE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"message": MSG_SHUTTING_DOWN_INSTANCE}, status=status.HTTP_200_OK)


class InstanceSecurityGroup(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = SecurityGroupSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        ret = self.serializer_class(instance.security_groups.all(), many=True)
        proposal_accounts = [i.username for i in instance.associated_proposals.all()]
        ret_data = ret.data + proposal_accounts
        return Response(ret_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sec_group_name = serializer.validated_data["name"]

        try:
            sec_group = security_groups_service.get_by_field("name", sec_group_name)
        except SecurityGroup.DoesNotExist:
            if sec_group_name.startswith("u"):
                try:
                    proposal_account = ProposalAccount.objects.get(username=f"{sec_group_name}")
                    instance.associated_proposals.add(proposal_account)
                except ProposalAccount.DoesNotExist:
                    return Response(data={"message": MSG_SECURITY_GROUP_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data={"message": MSG_SECURITY_GROUP_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        else:
            instance.security_groups.add(sec_group)
        instance.save()
        return Response({"message": MSG_ADDED_SECURITY_GROUP}, status=status.HTTP_200_OK)


class InstanceSecurityGroupRemove(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = SecurityGroupSerializer

    def get_object(self):
        if "instance_id" in self.kwargs:
            instance_id = self.kwargs["instance_id"]
            return default_model_class.objects.get(pk=instance_id)
        return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sec_group_name = serializer.validated_data["name"]
        proposal_account = None
        sec_group = None
        try:
            sec_group = security_groups_service.get_by_field("name", sec_group_name)
        except SecurityGroup.DoesNotExist:
            if sec_group_name.startswith("u"):
                try:
                    proposal_account = ProposalAccount.objects.get(username=f"{sec_group_name}")
                except ProposalAccount.DoesNotExist:
                    return Response(data={"message": MSG_SECURITY_GROUP_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data={"message": MSG_SECURITY_GROUP_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)

        if sec_group and sec_group not in instance.security_groups.all():
            return Response(data={"message": MSG_SECURITY_GROUP_NOT_ASSIGNED_IN_INSTANCE},
                            status=status.HTTP_400_BAD_REQUEST)
        elif sec_group:
            instance.security_groups.remove(sec_group)
            instance.save()
            return Response({"message": MSG_REMOVED_SECURITY_GROUP}, status=status.HTTP_200_OK)

        if proposal_account and proposal_account in instance.associated_proposals.all():
            instance.associated_proposals.remove(proposal_account)
            instance.save()
        else:
            return Response(data={"message": MSG_SECURITY_GROUP_NOT_ASSIGNED_IN_INSTANCE},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": MSG_REMOVED_SECURITY_GROUP}, status=status.HTTP_200_OK)
