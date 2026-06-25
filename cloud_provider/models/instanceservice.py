from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import instance_service as labels

logger: logging.Logger = logging.getLogger(__name__)


class InstanceService(TemplateModel):
    class PullPolicy(models.TextChoices):
        ALWAYS = "Always"
        IF_NOT_PRESENT = "IfNotPresent"
        NEVER = "Never"

    class Protocol(models.TextChoices):
        TCP = "TCP"
        UDP = "UDP"

    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    port = models.IntegerField(verbose_name=labels.MODEL_LABELS["port"])
    bind_address = models.GenericIPAddressField(
        verbose_name=labels.MODEL_LABELS["bind_address"])
    protocol = models.CharField(choices=Protocol.choices, max_length=50, verbose_name=labels.MODEL_LABELS["protocol"])
    sidecar_deployed = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["sidecar_deployed"])
    container_image = models.CharField(max_length=255, null=True, blank=True,
                                       verbose_name=labels.MODEL_LABELS["container_image"])
    cpu_requests = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["cpu_requests"])
    memory_requests = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["memory_requests"])
    cpu_limits = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["cpu_limits"])
    memory_limits = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["memory_limits"])
    env_string = models.TextField(null=True, blank=True, verbose_name=labels.MODEL_LABELS["env_string"])
    command = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["command"])
    args = models.TextField(null=True, blank=True, verbose_name=labels.MODEL_LABELS["args"])
    pull_secrets_name = models.CharField(max_length=255, null=True, blank=True,
                                         verbose_name=labels.MODEL_LABELS["pull_secrets_name"])
    pull_policy = models.CharField(choices=PullPolicy.choices, max_length=50, null=True, blank=True)
    mount_pvc_storage = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["mount_pvc_storage"])
    mount_tmp_dir = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["mount_tmp_dir"])
    mount_scratch_dir = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["mount_scratch_dir"])
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = labels.VERBOSE_NAME
