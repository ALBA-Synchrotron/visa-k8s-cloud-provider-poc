import logging

from object_template.forms.my_object_name_filter import MyObjectNameFilterForm
from object_template.models import MyObjectName
from object_template.tests.utils.generic_form_test_case import MyGenericFormTestCase


class MyObjectNameFilterFormTest(MyGenericFormTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['my_object_name.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        super(MyObjectNameFilterFormTest, self).setUp()

        self.model_class = MyObjectName
        self.form_class = MyObjectNameFilterForm
        self.model_name = 'my_object_name'
        self.valid_json = {'name': 'Z Fighters'}

        self.logger.debug('#### setUp END ####')

    def test_valid(self):
        self.valid()
