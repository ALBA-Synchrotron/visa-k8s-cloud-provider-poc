from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from . import InstanceService
from ..labels.model import flavour as labels

logger: logging.Logger = logging.getLogger(__name__)


class Flavour(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    cpus = models.IntegerField(verbose_name=labels.MODEL_LABELS["cpus"])
    disk = models.IntegerField(verbose_name=labels.MODEL_LABELS["disk"])
    ram = models.FloatField(verbose_name=labels.MODEL_LABELS["ram"])
    instance_services = models.ManyToManyField(InstanceService, blank=True,
                                               verbose_name=labels.MODEL_LABELS["instance_services"])
    deleted = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["deleted"])
    mount_pvc_storage = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["mount_pvc_storage"])
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = labels.VERBOSE_NAME
