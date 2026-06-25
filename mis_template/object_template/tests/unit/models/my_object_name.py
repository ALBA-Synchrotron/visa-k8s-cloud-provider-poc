import logging

from object_template.models import MyObjectName
from object_template.tests.utils.generic_model_test_case import MyGenericModelTestCase


class MyObjectNameModelTest(MyGenericModelTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['my_object_name.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        super(MyObjectNameModelTest, self).setUp()

        self.model_class = MyObjectName
        self.model_name = 'my_object_name'
        self.mandatory_fields_json = {
            'name': 'MyObjectName 1'
        }
        self.all_fields_json = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id = 1
        self.update_json = {'name': 'Updated my_object_name'}

        self.logger.debug('#### setUp END ####')

    def test_create(self):
        self.create()

    def test_update(self):
        self.update()
