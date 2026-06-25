from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import security_group as labels

logger: logging.Logger = logging.getLogger(__name__)


class SecurityGroup(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = labels.VERBOSE_NAME
