# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from cloud_provider.labels.model import flavour as labels
from cloud_provider.models import Flavour
from cloud_provider.serializers.flavour import FlavourSerializer
from cloud_provider.services.flavour import FlavourService

default_model_class = Flavour
default_service = FlavourService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
default_permission_content_type_name = "flavour"


class FlavoursList(ListAPIView):
    queryset = default_model_class.objects.filter(deleted=False)
    serializer_class = FlavourSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]


class FlavourDetail(RetrieveAPIView):
    serializer_class = FlavourSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        if "flavour_id" in self.kwargs:
            flavour_id = self.kwargs["flavour_id"]
            return default_model_class.objects.get(pk=flavour_id, deleted=False)
        return None


class FlavourDeviceAllocations(RetrieveAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        if "flavour_id" in self.kwargs:
            flavour_id = self.kwargs["flavour_id"]
            return default_model_class.objects.get(pk=flavour_id, deleted=False)
        return None

    def get(self, _request, *_args, **_kwargs):
        _ = self.get_object()
        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.
        return Response(data=[], status=status.HTTP_200_OK)
