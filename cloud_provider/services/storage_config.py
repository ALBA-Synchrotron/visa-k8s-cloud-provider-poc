# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.services import GenericService
from ..labels.model import storage_config as labels
from ..models import StorageConfig


class StorageConfigService(GenericService):
    def __init__(self):
        GenericService.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.model_name = "StorageConfig"
        self.model_class = StorageConfig
        self.id_not_null = "%s %s" % (self.model_class, labels.ID_NOT_NULL)
