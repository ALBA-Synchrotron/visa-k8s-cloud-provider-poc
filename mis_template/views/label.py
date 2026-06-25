# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.serializers.label import LabelSerializer
from mis_template.services.label import LabelService
from mis_template.utils.authentication import CSRFExemptSSOAuthenticatedListAPIView, \
    CSRFExemptSSOAuthenticatedRetrieveAPIView
from mis_template.utils.request import ErrorFormatting

service = LabelService()
errorFormatting = ErrorFormatting()
logger = logging.getLogger(__name__)

default_serializer_class = LabelSerializer


class GetAll(CSRFExemptSSOAuthenticatedListAPIView):
    serializer_class = default_serializer_class
    pagination_class = None

    def get_queryset(self):
        return service.get_all()

    def get(self, request, *args, **kwargs):
        return super(GetAll, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetById(CSRFExemptSSOAuthenticatedRetrieveAPIView):
    serializer_class = default_serializer_class

    def has_permission(self):
        return True

    def get_object(self):
        object_id = self.kwargs.get('object_id')
        return service.get_by_pk(object_id)

    def get(self, request, *args, **kwargs):
        return super(GetById, self).get(request, *args, **kwargs)
