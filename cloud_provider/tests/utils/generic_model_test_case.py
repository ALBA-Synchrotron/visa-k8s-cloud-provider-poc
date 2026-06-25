# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_model_test_case import GenericModelTestCase

logger = logging.getLogger(__name__)


class MyGenericModelTestCase(GenericModelTestCase):
    logger = logging.getLogger(__name__)
