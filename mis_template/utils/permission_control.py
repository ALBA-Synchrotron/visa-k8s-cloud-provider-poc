# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from cloud_provider.labels.generic import generic as labels

logger = logging.getLogger(__name__)


def get_or_create_permission(codename, name, content_type):
    permission = Permission.objects.filter(content_type=content_type, codename=codename).first()

    if not permission:
        permission = Permission.objects.create(content_type=content_type, codename=codename, name=name)
        print('Created Permission: %s in content type: %s' % (permission, content_type,))
    else:
        print('Found Permission: %s in ContentType: %s' % (permission, content_type,))

    return permission


def get_or_create_content_type(app_label, model):
    content_type = ContentType.objects.filter(app_label=app_label, model=model).first()
    if not content_type:
        content_type = ContentType.objects.create(app_label=app_label, model=model)
        print('Created ContentType: %s' % content_type)
    else:
        print('Found ContentType: %s' % content_type)

    return content_type


def create_group(group_name):
    print('Getting %s group' % group_name)
    try:
        group = get(name=group_name)
    except Group.DoesNotExist:
        Group(name=group_name).save()
        group = get(name=group_name)
        print('%s group got' % group_name)
    return group


def create_group_permissions(group_name, app_label, model_name, operations_list):
    group = create_group(group_name)

    print(
        'Assigning %s permissions from model %s.%s to %s group' % (operations_list, app_label, model_name, group_name))
    content_type = get_or_create_content_type(app_label, model_name)
    for operation_name in operations_list:
        permission = get_or_create_permission('%s_%s' % (operation_name, model_name),
                                              'Can %s %s' % (operation_name, model_name), content_type)
        try:
            group.permissions.add(permission)
        except Exception as e:
            print(e)
            print('Permission already assigned to group')
    print(
        '%s permissions from model %s.%s to %s group assigned!' % (operations_list, app_label, model_name, group_name))


def create_group_permissions_by_json_data(json_path):
    with transaction.atomic():
        try:
            data = open(json_path).read()
            json_data_list = json.loads(data)
        except Exception as e:
            logging.error(e)
            json_data_list = []

    for json_data_element in json_data_list:
        group_name = getattr(settings, json_data_element['group_settings_name'])
        app_label = json_data_element['app_label']
        model_name = json_data_element['model_name']
        operations_list = json_data_element['operations_list'].split(',')
        create_group_permissions(group_name, app_label, model_name, operations_list)


def add_users_to_group(group_name, users_list):
    print('Getting %s group' % group_name)
    try:
        group = get(name=group_name)
    except Group.DoesNotExist:
        Group(name=group_name).save()
        group = get(name=group_name)
        print('%s group got' % group_name)

    print('-Adding users to group %s' % group_name)
    for username in users_list:
        with transaction.atomic():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username)
            except Exception as ie:
                print(labels.CONTROLLED_ERROR % ie)
                user = get(username=username)
            user.save()
            group.user_set.add(user.id)


def add_users_to_group_by_json_data(json_path):
    with transaction.atomic():
        try:
            data = open(json_path).read()
            json_data_list = json.loads(data)
        except Exception as e:
            logging.error(e)
            json_data_list = []

        for json_data_element in json_data_list:
            group_name = getattr(settings, json_data_element['group_settings_name'])
            users_list = json_data_element['users_list'].split(',')
            add_users_to_group(group_name, users_list)


class UserMembership:
    """
    An UserMembership that checks if the user can edit/create/enable/disable item types
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.year = date.today().year

    def is_user_in_group(self, user_name=None, group_name=None):
        try:
            return user_name and User.objects.filter(username=user_name, groups__name=group_name).exists()
        except Exception as e:
            self.logger.error(e)
            raise e

    def is_user_in_groups_list(self, user_name=None, group_name_list=None):
        try:
            for group_name in group_name_list:
                if user_name and User.objects.filter(username=user_name, groups__name=group_name).exists():
                    return True
            return False
        except Exception as e:
            self.logger.error(e)
            raise e
