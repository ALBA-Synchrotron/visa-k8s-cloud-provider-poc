import logging
import os
import shutil
from re import split
from shutil import copyfile

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    template_app_name = 'mis_template'
    template_directory_name = 'object_template'
    template_model_name = 'my_object_name'

    help = 'Crates a default object ad all needed to work with django with a simple setup'

    def add_arguments(self, parser):
        parser.add_argument('--app_name', dest='app_name', default='',
                            help='The model name in lower case and separated by underscore')
        parser.add_argument('--model_name', dest='model_name', default='',
                            help='The model name in lower case and separated by underscore')

    def handle(self, *args, **options):
        logger.debug('###############################################################')
        logger.debug('###### DJANGO CUSTOM COMMAND create object from template ######')
        logger.debug('###############################################################')
        logger.info('object_from_template.py start')

        app_name = options['app_name']
        model_name = options['model_name']

        self.create_labels_file(app_name, model_name)
        self.create_model_file(app_name, model_name)
        self.create_form_file(app_name, model_name)
        self.create_form_filter_file(app_name, model_name)
        self.create_service_file(app_name, model_name)
        self.create_view_file(app_name, model_name)
        self.create_url_file(app_name, model_name)
        self.create_template_directory(app_name, model_name)
        self.create_test_file(app_name, model_name)

        logger.info('object_from_template.py end')
        logger.debug('########################################################################')

    @staticmethod
    def get_camelcase_name(name):
        name_list = [a.capitalize() for a in split('([^a-zA-Z0-9])', name) if a.isalnum()]
        return ''.join(name_list)

    @staticmethod
    def get_verbose_name(name):
        name_list = [a.capitalize() for a in split('([^a-zA-Z0-9])', name) if a.isalnum()]
        return ' '.join(name_list)

    def check_or_create_directory(self, path_name):
        if not os.path.exists(path_name):
            os.mkdir(path_name)
            init_file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name,
                                            '__init__.py')
            init_file_destination = os.path.join(path_name, '__init__.py')
            copyfile(init_file_origin, init_file_destination)

    def replace_model_name(self, file_name, app_name, model_name, extension='.py'):
        origin_file_name = file_name.replace(extension, '_bk' + extension)
        copyfile(file_name, origin_file_name)

        file_input = open(origin_file_name, "rt")
        file_output = open(file_name, "wt")
        for line in file_input:
            new_line = line.replace(self.template_directory_name, app_name)
            new_line = new_line.replace(self.template_model_name, model_name)
            new_line = new_line.replace(self.get_camelcase_name(self.template_model_name),
                                        self.get_camelcase_name(model_name))
            new_line = new_line.replace(self.get_verbose_name(self.template_model_name),
                                        self.get_verbose_name(model_name))
            file_output.write(new_line)
        file_input.close()
        file_output.close()

        os.remove(origin_file_name)

    def copy_file(self, file_origin, file_destination, app_name, model_name):
        try:
            copyfile(file_origin, file_destination)
            name, extension = os.path.splitext(file_destination)
            self.replace_model_name(file_destination, app_name, model_name, extension)
        except shutil.SameFileError:
            pass

    def create_generic_file(self, app_name, model_name, directory_name):
        path_destination = os.path.join(settings.BASE_DIR, app_name, directory_name)
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name,
                                   directory_name, 'my_object_name.py')
        file_destination = os.path.join(settings.BASE_DIR, app_name, directory_name, model_name + '.py')
        self.copy_file(file_origin, file_destination, app_name, model_name)

    def create_labels_file(self, app_name, model_name):
        labels_path_destination = os.path.join(settings.BASE_DIR, app_name, 'labels')
        self.check_or_create_directory(labels_path_destination)
        model_path_destination = os.path.join(settings.BASE_DIR, app_name, 'labels', 'model')
        self.check_or_create_directory(model_path_destination)
        model_label_file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name,
                                               'labels', 'model', 'my_object_name.py')
        model_label_file_destination = os.path.join(settings.BASE_DIR, app_name, 'labels', 'model', model_name + '.py')
        self.copy_file(model_label_file_origin, model_label_file_destination, app_name, model_name)

    def create_model_file(self, app_name, model_name):
        self.create_generic_file(app_name, model_name, 'models')

        init_file_destination = os.path.join(settings.BASE_DIR, app_name, 'models', '__init__.py')
        new_line = 'from .%s import %s\n' % (model_name, self.get_camelcase_name(model_name))
        with open(init_file_destination, 'a') as a_file:
            a_file.write("\n")
            a_file.write(new_line)

    def create_form_file(self, app_name, model_name):
        self.create_generic_file(app_name, model_name, 'forms')

    def create_form_filter_file(self, app_name, model_name):
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'forms')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'forms',
                                   'my_object_name_filter.py')
        file_destination = os.path.join(settings.BASE_DIR, app_name, 'forms', model_name + '_filter.py')
        self.copy_file(file_origin, file_destination, app_name, model_name)

    def create_service_file(self, app_name, model_name):
        self.create_generic_file(app_name, model_name, 'services')

    def create_view_file(self, app_name, model_name):
        self.create_generic_file(app_name, model_name, 'views')

    def create_url_file(self, app_name, model_name):
        self.create_generic_file(app_name, model_name, 'urls')

    def copy_template_file(self, app_name, model_name, file_name):
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'templates',
                                   file_name + '.html')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'templates', app_name, model_name,
                                        file_name + '.html')
        self.copy_file(file_origin, path_destination, app_name, model_name)

    def create_template_directory(self, app_name, model_name):
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'templates')
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'templates', app_name)
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'templates', app_name, model_name)
        self.check_or_create_directory(path_destination)

        self.copy_template_file(app_name, model_name, 'delete')
        self.copy_template_file(app_name, model_name, 'detail')
        self.copy_template_file(app_name, model_name, 'form')
        self.copy_template_file(app_name, model_name, 'list')

    def copy_views_template_file(self, app_name, model_name, file_name):
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'unit', 'views', 'my_object_name', file_name + '.py')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'views', model_name,
                                        'test_' + file_name + '.py')
        self.copy_file(file_origin, path_destination, app_name, model_name)

    def create_test_file(self, app_name, model_name):
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', )
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'fixtures')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'fixtures', 'my_object_name.json')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'fixtures', model_name + '.json')
        self.copy_file(file_origin, path_destination, app_name, model_name)

        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit')
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'forms')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'unit', 'forms', 'my_object_name.py')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'forms',
                                        'test_' + model_name + '.py')
        self.copy_file(file_origin, path_destination, app_name, model_name)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'unit', 'forms', 'my_object_name_filter.py')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'forms',
                                        'test_' + model_name + '_filter.py')
        self.copy_file(file_origin, path_destination, app_name, model_name)

        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'models')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'unit', 'models', 'my_object_name.py')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'models',
                                        'test_' + model_name + '.py')
        self.copy_file(file_origin, path_destination, app_name, model_name)

        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'services')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'unit', 'services', 'my_object_name.py')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'services',
                                        'test_' + model_name + '.py')
        self.copy_file(file_origin, path_destination, app_name, model_name)

        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'views')
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'unit', 'views', model_name)
        self.check_or_create_directory(path_destination)

        self.copy_views_template_file(app_name, model_name, 'delete')
        self.copy_views_template_file(app_name, model_name, 'detail')
        self.copy_views_template_file(app_name, model_name, 'list')
        self.copy_views_template_file(app_name, model_name, 'new')
        self.copy_views_template_file(app_name, model_name, 'update')

        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'acceptance')
        self.check_or_create_directory(path_destination)
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'acceptance', 'features')
        self.check_or_create_directory(path_destination)
        file_origin = os.path.join(settings.BASE_DIR, self.template_app_name, self.template_directory_name, 'tests',
                                   'acceptance', 'features', 'my_object_name.feature')
        path_destination = os.path.join(settings.BASE_DIR, app_name, 'tests', 'acceptance', 'features', model_name + '.feature')
        self.copy_file(file_origin, path_destination, app_name, model_name)
