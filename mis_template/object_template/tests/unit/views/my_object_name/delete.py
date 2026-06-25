import logging

from object_template.labels.model import my_object_name as labels

from object_template.forms.my_object_name import MyObjectNameForm
from object_template.models import MyObjectName
from object_template.tests.utils.generic_view_test_case import MyGenericViewTest


# forms test
class MyObjectNameViewTest(MyGenericViewTest):
    logger = logging.getLogger(__name__)
    fixtures = ['my_object_name.json']

    def setUp(self):
        super(MyObjectNameViewTest, self).setUp()
        self.logger.debug('#### setUp START ####')

        self.model_name = 'MyObjectName'
        self.reference_name = 'my_object_name'

        self.labels = labels

        self.is_cas_authenticated = True
        self.check_unauthorized_user = True
        self.check_authorized_user_list = [self.app_admin_username, self.app_manager_username]

        self.existing_object = 1
        self.not_existing_object = 9999

        self.form_class = MyObjectNameForm
        self.template_directory_name = labels.APP_NAME + '/' + labels.MODEL_NAME + '/'

        self.model_class = MyObjectName

        self.logger.debug('#### setUp END ####')

    def test_delete(self):
        self.delete()
