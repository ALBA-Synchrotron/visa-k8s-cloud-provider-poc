# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from cloud_provider.labels.model import security_group as labels
from cloud_provider.models import SecurityGroup
from cloud_provider.serializers.instance_security_group_svc import InstanceSecurityGroupSVCSerializer
from cloud_provider.services.security_group import SecurityGroupService

default_model_class = SecurityGroup
default_service = SecurityGroupService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
default_permission_content_type_name = "instance_security_group"


class InstanceSecurityGroups(GenericAPIView):
    queryset = default_model_class.objects.all()
    serializer_class = InstanceSecurityGroupSVCSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]

    def post(self, request, *args, **kwargs):
        # Retrieve instance data with instance serializer
        serializer_data = self.serializer_class(data=request.data)
        if not serializer_data.is_valid():
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer_class().to_representation(serializer_data.validated_data), status=status.HTTP_200_OK)