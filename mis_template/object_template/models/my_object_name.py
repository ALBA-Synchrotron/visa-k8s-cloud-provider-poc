from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import my_object_name as labels

logger = logging.getLogger(__name__)


class MyObjectName(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS['name'])
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = labels.VERBOSE_NAME
