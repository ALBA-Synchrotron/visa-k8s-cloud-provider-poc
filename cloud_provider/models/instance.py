from __future__ import unicode_literals

import logging

from django.db import models
from simple_history.models import HistoricalRecords

from mis_template.utils.models import TemplateModel
from . import SecurityGroup
from ..labels.model import instance as labels

logger: logging.Logger = logging.getLogger(__name__)


class Instance(TemplateModel):
    name = models.CharField(max_length=50, verbose_name=labels.MODEL_LABELS["name"])
    flavour = models.ForeignKey("Flavour", verbose_name=labels.MODEL_LABELS["flavour"], on_delete=models.PROTECT)
    image = models.ForeignKey("Image", verbose_name=labels.MODEL_LABELS["image"], on_delete=models.PROTECT)
    active = models.BooleanField(default=True, verbose_name=labels.MODEL_LABELS["active"])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=labels.MODEL_LABELS["created_at"])
    updated_at = models.DateTimeField(auto_now=True, verbose_name=labels.MODEL_LABELS["updated_at"])
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=labels.MODEL_LABELS["deleted_at"])
    visa_uid = models.CharField(max_length=50, default="", blank=True, null=True,
                                verbose_name=labels.MODEL_LABELS["visa_uid"])
    # This field ("address") is automatically retrieved from Kubernetes, it can be set directly through the database just to override
    # the origin of this field. This is done through the serializer.
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name=labels.MODEL_LABELS["address"])
    security_groups = models.ManyToManyField(SecurityGroup, blank=True,
                                             verbose_name=labels.MODEL_LABELS["security_groups"])
    deployment_name = models.CharField(max_length=100, blank=True, null=True,
                                       verbose_name=labels.MODEL_LABELS["deployment_name"])
    deployment_representation = models.JSONField(verbose_name=labels.MODEL_LABELS["deployment_representation"],
                                                 null=True, blank=True)
    associated_proposals = models.ManyToManyField("ProposalAccount", blank=True,
                                                  verbose_name=labels.MODEL_LABELS["associated_proposals"])
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = labels.VERBOSE_NAME
