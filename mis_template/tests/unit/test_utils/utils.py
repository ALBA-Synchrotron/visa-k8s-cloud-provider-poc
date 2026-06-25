import json
import logging
import os

from django.conf import settings
from django.core import serializers

from mis_template.utils.test.generic_test_case import GenericTestCase


class GenericUtilsTestCase(GenericTestCase):
    logger = logging.getLogger(__name__)

    rack_fixtures = ['system.json', 'subsystem.json', 'racktype.json', 'rackstatus.json', 'location.json',
                     'location_place.json', 'rack.json', 'connection_type.json']

    test_directory = os.path.join(settings.BASE_DIR, 'cabledb', 'tests', 'unit', 'documents')

    def model_formset_to_request_json(self, formset_list, formset_name):
        self.logger.debug(formset_list)
        serialized_model_json_list = json.loads(serializers.serialize('json', formset_list))
        result_json = {formset_name + '-TOTAL_FORMS': len(serialized_model_json_list),
                       formset_name + '-INITIAL_FORMS': len(serialized_model_json_list),
                       formset_name + '-MIN_NUM_FORMS': '0', formset_name + '-MAX_NUM_FORMS': '1000'}
        for index, serialized_model_json in enumerate(serialized_model_json_list):
            prefix = '%s-%s-' % (formset_name, index)
            for key, value in serialized_model_json.items():
                if key == 'pk':
                    result_json[prefix + 'id'] = value
                if key == 'fields':
                    for fields_key, fields_value in value.items():
                        result_json[prefix + fields_key] = fields_value
            result_json[prefix + 'DELETE'] = ''

        if serialized_model_json_list:
            last_element = len(serialized_model_json_list)
        else:
            last_element = 0
        return result_json, last_element

    def formset_to_request_json(self, formset_list, formset_name):
        self.logger.debug(formset_list)

        result_json = {formset_name + '-TOTAL_FORMS': len(formset_list),
                       formset_name + '-INITIAL_FORMS': len(formset_list),
                       formset_name + '-MIN_NUM_FORMS': '0', formset_name + '-MAX_NUM_FORMS': '1000'}

        for index, formset in enumerate(formset_list):
            prefix = '%s-%s-' % (formset_name, index)
            if formset:
                for key, value in formset.data():
                    if key == 'pk':
                        result_json[prefix + 'id'] = value
                    if key == 'fields':
                        for fields_key, fields_value in value.items():
                            result_json[prefix + fields_key] = fields_value
                result_json[prefix + 'DELETE'] = ''

        if formset_list:
            last_element = len(formset_list)
        else:
            last_element = 0
        return result_json, last_element
