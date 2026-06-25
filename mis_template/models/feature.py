# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel

logger = logging.getLogger(__name__)


class Feature(TemplateModel):
    code = models.CharField(max_length=150, unique=True, verbose_name='code')
    description = models.CharField(max_length=150, null=True, blank=True, default=None, verbose_name='description')
    enabled = models.BooleanField(default=False, verbose_name='enabled')
    history = HistoricalRecords()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Feature'
