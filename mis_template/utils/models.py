# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.db import models, transaction
from django.forms.models import model_to_dict

from mis_template.utils.utils import beautify_string
from cloud_provider.labels.generic import generic as labels

logger = logging.getLogger(__name__)


class TemplateModel(models.Model):
    def get_fields(self):
        res = []
        for field in self.__class__._meta.fields:
            res.append((beautify_string(field.verbose_name), str(getattr(self, field.name))))
        return res

    def get_fields_raw(self):
        res = []
        for field in self.__class__._meta.fields:
            res.append((beautify_string(field.verbose_name), getattr(self, field.name)))
        return res

    def get_m2m_fields(self):
        res = []
        for field in self.__class__._meta.many_to_many:
            result_value = list(map(lambda m2m_field: str(m2m_field), getattr(self, field.name).all()))
            res.append((beautify_string(field.verbose_name), result_value))
        return res

    class Meta:
        abstract = True


def get_or_create_model(json_data_element, model_class, service_class, get_field_name):
    try:
        element = service_class().get_by_field(get_field_name, json_data_element[get_field_name])
    except model_class.DoesNotExist as dne:
        logger.debug(labels.CONTROLLED_ERROR % dne)
        element = model_class.objects.create(**json_data_element)
    except Exception as e:
        logger.error(str(e))
        element = None
    return element


def create_or_update_model(json_data_element, model_class, service_class, get_field_name, foreign_key_name=[],
                           foreign_key_model=[]):
    foreign_key_values = []
    try:
        for fk_name in foreign_key_name:
            foreign_key_values.append(json_data_element.pop(fk_name, None))
    except Exception as e:
        logger.error(e)
    try:
        element = service_class().get_by_field(get_field_name, json_data_element[get_field_name])
        for key, value in json_data_element.items():
            setattr(element, key, value)
        if len(foreign_key_values):
            for index, fk_value in enumerate(foreign_key_values):
                try:
                    fk_object = foreign_key_model[index].objects.get(pk=fk_value)
                except IndexError:
                    fk_object = None
                if fk_object:
                    setattr(element, foreign_key_name[index], fk_object)
        element.save()
    except model_class.DoesNotExist as dne:
        logger.debug(labels.CONTROLLED_ERROR % dne)
        if len(foreign_key_values):
            for index, fk_value in enumerate(foreign_key_values):
                try:
                    fk_object = foreign_key_model[index].objects.get(pk=fk_value)
                except IndexError:
                    fk_object = None
                if fk_object:
                    json_data_element[foreign_key_name[index]] = fk_object
        element = model_class.objects.create(**json_data_element)
    except Exception as e:
        logger.error(str(e))
        element = None
    return element


def create_or_update_model_by_json_data(json_path, model_class, service_class, get_field_name, foreign_key_name=[],
                                        foreign_key_model=[]):
    try:
        data = open(json_path).read()
        json_data_list = json.loads(data)
    except Exception as e:
        logging.error(e)
        json_data_list = []

    with transaction.atomic():
        # Create absence types:
        logger.debug('- Creating default %s' % model_class._meta.object_name)

        for json_data_element in json_data_list:
            create_or_update_model(json_data_element, model_class, service_class, get_field_name, foreign_key_name,
                                   foreign_key_model)


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])
