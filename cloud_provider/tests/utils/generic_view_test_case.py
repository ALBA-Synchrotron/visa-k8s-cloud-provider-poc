# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_view_test_case import GenericViewTest
from cloud_provider.labels.generic import generic as labels


class MyGenericViewTest(GenericViewTest):
    logger = logging.getLogger(__name__)

    app_admin_username = 'dsalvat'
    app_manager_username = 'vgarrido'
    app_user_username = 'omatilla'
    app_nonauthorized_username = 'nouser'

    all_roles_list = [app_admin_username, app_manager_username, app_nonauthorized_username]
