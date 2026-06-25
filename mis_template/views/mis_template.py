# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.shortcuts import render

from settings import labels
from mis_template.utils.permission_control import UserMembership
from mis_template.utils.template_views import AuthenticatedTemplateView

logger = logging.getLogger(__name__)
template_directory_name = 'mis_template/'


def default_context_data(context_data):
    context_data['labels'] = labels
    return context_data
