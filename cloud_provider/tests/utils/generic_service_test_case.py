# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_service_test_case import GenericServiceTest


class MyGenericServiceTest(GenericServiceTest):
    logger = logging.getLogger(__name__)
