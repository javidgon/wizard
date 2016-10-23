from jinja2 import Environment, PackageLoader
from subprocess import call
import yaml
import os
import shutil


def _write_rendered_file(filepath, template, **kwargs):
    """
    Write a rendered file to a certain path.
    """
    f = open(filepath, 'w')
    print >> f, template.render(**kwargs)
    f.close()


def setup_global_project_conf(project):
    """
    Setup global Project configuration like requirements or extra files.
    """
    # Configure for Heroku (if required)
    if project.get('deployable_in_heroku'):
	_write_rendered_file('Procfile', procfile_template, project=project)

    # Create REQUIREMENTS.txt file
    _write_rendered_file(
        'requirements.txt',
         requirements_template,
         deployable_in_heroku=project.get('deployable_in_heroku'))


def setup_statics(project, frontend):
    """
    Setup Statics like JS or LESS files (depending on the frontend)
    """
    # Create JS Static structure
    static_path = '{}/static/js'.format(project.get('name'))
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    if frontend == 'angular':
        _write_rendered_file('{}/app.js'.format(static_path),
                             app_static_template,
                             project=project)
        _write_rendered_file('{}/services.js'.format(static_path),
                             services_static_template,
                             apps=apps)
        _write_rendered_file('{}/controllers.js'.format(static_path),
                             controllers_static_template,
                             apps=apps)

        # Create Partials Static structure
        angular_templates_path = '{}/static/partials'.format(project.get('name'))
        if not os.path.exists(angular_templates_path):
            os.makedirs(angular_templates_path)

        shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                    'scaffolder/templates/static/partials/home.html',
                    '{}/home.html'.format(angular_templates_path))

    # Create Less Static structure
    less_static_path = '{}/static/less'.format(project.get('name'))
    if not os.path.exists(less_static_path):
        os.makedirs(less_static_path)

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                'scaffolder/templates/static/less/styles.less',
                '{}/styles.less'.format(less_static_path))


def setup_main_django_app(project, frontend):
    """
    Setup common views and urls of the main django application.
    The code processed here comes from utilities like UserToken or
    the Initial View.
    """
    project_name = project.get('name') 
    # Connect the different applications with the main URLS.py File
    _write_rendered_file('{}/urls.py'.format(project_name),
                         main_urls_template,
                         apps=apps,
                         frontend=frontend)
    _write_rendered_file('{}/views.py'.format(project_name),
                         main_views_template)
    _write_rendered_file('{}/forms.py'.format(project_name),
                         main_forms_template)
    _write_rendered_file('{}/models.py'.format(project_name),
                         main_models_template,
                         project=project)

    # Create Django Template structure
    templates_path = '{}/templates'.format(project_name)
    if not os.path.exists(templates_path):
        os.makedirs(templates_path)

    # Create base.html
    if frontend == 'angular':
        shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                    'scaffolder/templates/html/base_angular.html',
                    '{}/base.html'.format(templates_path))
    else:
        shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                    'scaffolder/templates/html/base.html',
                    '{}/base.html'.format(templates_path))
        shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                    'scaffolder/templates/html/main.html',
                    '{}/main.html'.format(templates_path))


    # Add added applications to the SETTINGS.py file
    new_settings_file = ''
    for line in open("{}/settings.py".format(project.get('name'))).readlines():
        new_settings_file += line
        if line.startswith("    'django.contrib.staticfiles'"):
            for app in apps:
                new_settings_file += "    '{}.apps.{}Config',\n".format(
                    app.get('name'), app.get('name').capitalize())
            new_settings_file += "    '{}',\n".format(project.get('name'))

    f = open('{}/settings.py'.format(project.get('name')), 'w')
    print >> f, new_settings_file
    f.close()

    if project.get('deployable_in_heroku'):
        new_settings_file = ''
        for line in open("{}/settings.py".format(project.get('name'))).readlines():
            new_settings_file += line
            if line.startswith("    'django.contrib.messages',"):
                new_settings_file += "    'whitenoise.runserver_nostatic',\n"
            elif line.startswith("    'django.middleware.security.SecurityMiddleware',"):
                new_settings_file += "    'whitenoise.middleware.WhiteNoiseMiddleware',\n"
            elif line.startswith("STATIC_URL = '/static/'"):
                new_settings_file += "STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n"
                new_settings_file += "STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')\n"

    f = open('{}/settings.py'.format(project.get('name')), 'w')
    print >> f, new_settings_file
    f.close()


def setup_django_apps(apps, frontend):
    """
    Setup each of the Django applications configured by the user in the 'config.yml' file
    """
    for app in apps:
        call(["python", "manage.py", 'startapp', app.get('name')])

        app_name = app.get('name')
        # Create Static structure
        static_path = '{}/static'.format(app_name)
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        _write_rendered_file('{}/models.py'.format(app_name),
                             models_template,
                             project=project,
                             app=app)
        _write_rendered_file('{}/forms.py'.format(app_name),
                             forms_template,
                             app=app)
        _write_rendered_file('{}/admin.py'.format(app_name),
                             admin_template,
                             models=app.get('models'))

        # f = open('{}/tests.py'.format(app.get('name')), 'w')
        # print >> f, tests_template.render(app=app)
        # f.close()

        if frontend:
            _write_rendered_file('{}/api_urls.py'.format(app_name),
                                 api_urls_template,
                                 app=app)
            _write_rendered_file('{}/api.py'.format(app_name),
                                 api_template,
                                 app=app)
        else:
            _write_rendered_file('{}/urls.py'.format(app_name),
                                 urls_template,
                                 app=app)
            _write_rendered_file('{}/views.py'.format(app_name),
                                 views_template,
                                 app=app)
 
            # Create Django Template structure
            for model in app.get('models'):
                # TODO: Pluralization here is not really sophisticated
                model_templates_path = '{}/templates/{}s'.format(
                   app_name, model.get('name').lower())
                if not os.path.exists(model_templates_path):
                    os.makedirs(model_templates_path)

                # Create index.html and detail.html
                for page in ['index.html', 'detail.html']:
                    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                                'scaffolder/templates/html/{}'.format(page),
                                '{}/{}'.format(model_templates_path, page))


if __name__ == '__main__':
    # Load Configuration
    config = yaml.load(file('config.yml', 'r'))
    project = config.get('project')
    apps = project.get('apps')
    frontend = project.get('frontend') if project.get('frontend') != 'none' else None

    # Create Jinja2 Environment
    env = Environment(loader=PackageLoader('scaffolder', 'templates'))

    # Django
    main_urls_template = env.get_template('django/main_urls.py')
    main_views_template = env.get_template('django/main_views.py')
    main_forms_template = env.get_template('django/main_forms.py')
    main_models_template = env.get_template('django/main_models.py')
    models_template = env.get_template('django/models.py')
    views_template = env.get_template('django/views.py')
    urls_template = env.get_template('django/urls.py')
    api_urls_template = env.get_template('django/api_urls.py')
    api_template = env.get_template('django/api.py')
    forms_template = env.get_template('django/forms.py')
    admin_template = env.get_template('django/admin.py')
    # tests_template = env.get_template('django/tests.py')
    requirements_template = env.get_template('django/requirements.txt')

    # Heroku
    procfile_template = env.get_template('heroku/Procfile')

    # Statics
    app_static_template = env.get_template('static/js/app.js')
    services_static_template = env.get_template('static/js/services.js')
    controllers_static_template = env.get_template('static/js/controllers.js')

    # Start Scaffolding
    print "*******************************************************************"
    print "* Welcome to Wizard: Django Scaffolding Tool v0.2"
    print "*******************************************************************"
    print "0) Removing previous project... (if exists)"

    if os.path.exists('{}'.format(project.get('name'))):
        shutil.rmtree('{}'.format(project.get('name')))

    print "1) Creating Django '{}' Project...".format(project.get('name'))
    call(["django-admin", "startproject", project.get('name')])

    # Go inside the project.
    os.chdir(project.get('name'))

    print "2) Generating Project's Configuration..."
    setup_global_project_conf(project)
    print "3) Generating Project's Statics..."
    setup_statics(project, frontend)
    print "4) Creating Django Apps..."
    setup_django_apps(apps, frontend)
    print "5) Installing Common Settings..."
    setup_main_django_app(project, frontend)

    # Go back to the parent directory
    os.chdir('../')
    print "Done! Before running your Project please do the following steps:"
    print "1) Install dependencies by running 'pip install -r requirements.txt'"
    print "2) Make sure that the models have been properly generated"
    print "3) If so, create migrations by running 'python manage.py makemigrations'"
    print "4) Apply those migrations by running 'python manage.py migrate'"
    print "5) Create a superuser by login into 'python manage.py shell'"
    print "6) Enjoy!"
