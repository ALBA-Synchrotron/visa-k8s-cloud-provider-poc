from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import cloud_limit as labels

logger = logging.getLogger(__name__)


class CloudLimit(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    description = models.CharField(max_length=100, verbose_name=labels.MODEL_LABELS["description"])
    value = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["value"])
    unit = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["unit"])

    history = HistoricalRecords()

    class Meta:
        verbose_name = labels.VERBOSE_NAME
