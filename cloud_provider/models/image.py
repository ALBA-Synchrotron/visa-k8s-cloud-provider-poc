from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import image as labels

logger: logging.Logger = logging.getLogger(__name__)


class Image(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    full_image_url = models.CharField(max_length=255, verbose_name=labels.MODEL_LABELS["full_image_url"])
    size = models.FloatField(verbose_name=labels.MODEL_LABELS["size"])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=labels.MODEL_LABELS["created_at"])
    home_template_path = models.CharField(max_length=255, null=True,
                                          verbose_name=labels.MODEL_LABELS["home_template_path"])
    user_shell = models.CharField(max_length=255, null=True, verbose_name=labels.MODEL_LABELS["user_shell"])
    deleted = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["deleted"])
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=labels.MODEL_LABELS["deleted_at"])

    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = labels.VERBOSE_NAME
