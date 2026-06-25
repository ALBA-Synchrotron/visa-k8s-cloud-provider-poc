import logging

from object_template.labels.model import my_object_name as labels
from object_template.services.my_object_name import MyObjectNameService
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
        self.service_class = MyObjectNameService()

        self.labels = labels

        self.is_cas_authenticated = True
        self.check_unauthorized_user = True
        self.check_authorized_user_list = [self.app_admin_username, self.app_manager_username]

        self.list_filter_list = [{}]

        self.logger.debug('#### setUp END ####')

    def test_list(self):
        self.list()
