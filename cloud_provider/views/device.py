# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

"""
default_model_class = Flavour
default_service = FlavourService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
"""
default_permission_content_type_name = "device"



class DevicesList(ListAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        return None

    def get(self, _request, *_args, **_kwargs):
        _ = self.get_object()
        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.
        return Response(data=[], status=status.HTTP_200_OK)


class DeviceDetail(ListAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        return None

    def get(self, _request, *_args, **_kwargs):
        _ = self.get_object()
        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.
        return Response(data={}, status=status.HTTP_200_OK)

class DeviceAllocations(ListAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        return None

    def get(self, _request, *_args, **_kwargs):
        _ = self.get_object()
        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.
        return Response(data=[], status=status.HTTP_200_OK)