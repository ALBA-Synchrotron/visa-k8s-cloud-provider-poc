from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from ..labels.model import home_directory as labels

logger = logging.getLogger(__name__)


class HomeDirectory(TemplateModel):
    path = models.CharField(max_length=500, unique=True, null=False, blank=False,
                            verbose_name=labels.MODEL_LABELS["username"])
    proposal_account = models.ForeignKey("ProposalAccount", related_name="home_directory_list",
                                         verbose_name=labels.MODEL_LABELS["home_directory_list"],
                                         on_delete=models.DO_NOTHING)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.proposal_account.username}: {self.path}"

    class Meta:
        verbose_name = labels.VERBOSE_NAME
