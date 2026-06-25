from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import storage_config as labels

logger = logging.getLogger(__name__)


class StorageConfig(TemplateModel):
    instrument = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["instrument"])
    read_only = models.BooleanField(default=True, verbose_name=labels.MODEL_LABELS["read_only"])
    server = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["server"])
    server_path = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["server_path"])
    home_directory_prefix = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["home_directory_prefix"])
    extra_nfs_gids = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["extra_nfs_gids"])
    enabled = models.BooleanField(default=True, verbose_name=labels.MODEL_LABELS["enabled"])
    scratch_server = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["scratch_server"])
    scratch_server_path = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["scratch_server_path"])
    scratch_enabled = models.BooleanField(default=False, verbose_name=labels.MODEL_LABELS["scratch_enabled"])
    scratch_mount_path = models.CharField(max_length=50, null=True, blank=True, verbose_name=labels.MODEL_LABELS["scratch_mount_path"])
    scratch_read_only = models.BooleanField(default=True, verbose_name=labels.MODEL_LABELS["scratch_read_only"])

    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.instrument}-{self.server}"

    class Meta:
        verbose_name = labels.VERBOSE_NAME
