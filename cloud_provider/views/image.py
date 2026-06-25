# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from cloud_provider.labels.model import image as labels
from cloud_provider.models import Image
from cloud_provider.serializers.image import ImageSerializer
from cloud_provider.services.image import ImageService

default_model_class = Image
default_service = ImageService()
template_directory_name = labels.APP_NAME + "/" + labels.MODEL_NAME + "/"
default_permission_app_label_name = "cloud_provider"
default_permission_content_type_name = "image"


class ImagesList(ListAPIView):
    queryset = default_model_class.objects.filter(deleted=False)
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]


class ImageDetail(RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get_object(self):
        if "image_id" in self.kwargs:
            image_id = self.kwargs["image_id"]
            return default_model_class.objects.get(pk=image_id, deleted=False)
        return None
