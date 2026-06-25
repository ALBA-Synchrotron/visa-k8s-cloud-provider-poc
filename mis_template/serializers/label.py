# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import serializers

from mis_template.models.label import Label

logger = logging.getLogger(__name__)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Label
        extra_kwargs = {'id': {'required': False, }}
