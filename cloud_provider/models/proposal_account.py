from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import proposal_account as labels

logger = logging.getLogger(__name__)


class ProposalAccount(TemplateModel):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name=labels.MODEL_LABELS["username"])
    uid = models.CharField(max_length=50, null=False, blank=False, verbose_name=labels.MODEL_LABELS["uid"])
    gid = models.CharField(max_length=50, null=False, blank=False, verbose_name=labels.MODEL_LABELS["gid"])
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.username},uid={self.uid},gid={self.gid})"

    class Meta:
        verbose_name = labels.VERBOSE_NAME
