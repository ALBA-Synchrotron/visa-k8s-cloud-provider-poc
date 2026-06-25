# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from cloud_provider.labels.model import security_group as labels
from cloud_provider.models import SecurityGroup
from cloud_provider.serializers.security_group import SecurityGroupSerializer
from cloud_provider.services.security_group import SecurityGroupService

default_model_class = SecurityGroup
default_service = SecurityGroupService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
default_permission_content_type_name = "security_group"


class SecurityGroupList(ListAPIView):
    queryset = default_model_class.objects.all()
    serializer_class = SecurityGroupSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
