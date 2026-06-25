# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.services import GenericService
from ..labels.model import my_object_name as labels
from ..models import MyObjectName


class MyObjectNameService(GenericService):
    def __init__(self):
        GenericService.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.model_name = 'MyObjectName'
        self.model_class = MyObjectName
        self.id_not_null = '%s %s' % (self.model_class, labels.ID_NOT_NULL)
