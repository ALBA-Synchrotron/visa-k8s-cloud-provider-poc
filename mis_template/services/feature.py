# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from cloud_provider.labels.generic import generic as labels
from mis_template.utils.services import GenericService
from mis_template.models import Feature


class FeatureService(GenericService):
    def __init__(self):
        GenericService.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.model_name = 'Feature'
        self.model_class = Feature
        self.id_not_null = '%s %s' % (self.model_class, labels.ID_NOT_NULL)

    def is_feature_enabled(self, code):
        self.logger.debug('Checking if feature flag for %s is present and enabled' % code)
        result = self.model_class.objects.filter(code=code)
        return result.exists() and result.first().enabled