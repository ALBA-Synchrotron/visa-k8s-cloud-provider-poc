import logging

from object_template.forms.my_object_name import MyObjectNameForm
from object_template.models import MyObjectName
from object_template.tests.utils.generic_form_test_case import MyGenericFormTestCase


class MyObjectNameFormTest(MyGenericFormTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['my_object_name.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        super(MyObjectNameFormTest, self).setUp()

        self.model_class = MyObjectName
        self.form_class = MyObjectNameForm
        self.model_name = 'my_object_name'
        self.valid_json = {'name': 'Saiyan'}
        self.create_json = {'name': 'Saiyan'}

        self.logger.debug('#### setUp END ####')

    def test_empty(self):
        self.empty()

    def test_invalid(self):
        self.invalid()

    def test_valid(self):
        self.valid()

    def test_create(self):
        self.create()
