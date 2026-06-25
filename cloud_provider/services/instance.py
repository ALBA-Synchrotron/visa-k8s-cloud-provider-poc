# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.models import TemplateModel
from mis_template.utils.services import GenericService
from ..labels.model import instance as labels
from ..models import Instance


class InstanceService(GenericService):
    def __init__(self):
        GenericService.__init__(self)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.model_name: str = "Instance"
        self.model_class: TemplateModel = Instance
        self.id_not_null = "%s %s" % (self.model_class, labels.ID_NOT_NULL)
