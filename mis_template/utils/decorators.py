# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from functools import wraps
from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
from django.http import Http404

import settings.labels as labels
from mis_template.models import Feature
from mis_template.utils.permission_control import UserMembership

logger = logging.getLogger(__name__)
user_membership = UserMembership()


def permission_required(perm_name):
    def _permission_required(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(perm_name):
                raise PermissionDenied(labels.UNAUTHORIZED_USER)
            return view_func(request, *args, **kwargs)

        return wrapper

    return _permission_required


def any_permission_required(perms_name_list):
    def _any_permission_required(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if isinstance(perms_name_list, list):
                for perm_name in perms_name_list:
                    if request.user.has_perm(perm_name):
                        return view_func(request, *args, **kwargs)
            raise PermissionDenied(labels.UNAUTHORIZED_USER)

        return wrapper

    return _any_permission_required


def check_feature_flag(function=None, feature_code=None):
    """
    Decorator for views that checks whether the view should be displayed depending on
    a feature flag (or if the user can ignore feature flag restrictions). Returns a 404
    if the check is failed.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            logger.debug('In feature flag decorator')
            bypass_feature_flags = user_membership.is_user_in_groups_list(request.user.username,
                                                                          settings.BYPASS_FEATURE_FLAG_GROUP_LIST)
            logger.debug('%s can bypass feature flags: %s' % (request.user.username, bypass_feature_flags))
            if not bypass_feature_flags:
                logger.debug('Checking feature code: %s' % feature_code)
                feature_flag = Feature.objects.filter(code=feature_code)
                if not feature_flag.exists():
                    logger.warning('Checked for feature with code %s but could not find it' % feature_code)
                else:
                    if not feature_flag.first().enabled:
                        logger.debug('Feature not enabled, return 404')
                        raise Http404
                    logger.debug('Feature enabled, continue')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
