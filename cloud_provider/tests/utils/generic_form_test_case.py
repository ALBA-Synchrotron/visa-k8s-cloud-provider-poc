# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_form_test_case import GenericFormTestCase

logger = logging.getLogger(__name__)


class MyGenericFormTestCase(GenericFormTestCase):
    logger = logging.getLogger(__name__)
