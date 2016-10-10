from jinja2 import Environment, PackageLoader
from subprocess import call
import yaml
import os
import shutil


def setup_global_project_conf(project):
    # Configure for Heroku (if required)
    if project.get('deployable_in_heroku'):
        f = open('Procfile', 'w')
        print >> f, procfile_template.render(project=project)
        f.close()

    # Create REQUIREMENTS.txt file
    f = open('requirements.txt', 'w')
    print >> f, requirements_template.render(
        deployable_in_heroku=project.get('deployable_in_heroku'))
    f.close()


def setup_templates(project):
    # Create Django Template structure
    templates_path = '{}/templates'.format(project.get('name'))
    if not os.path.exists(templates_path):
        os.makedirs(templates_path)

    # Create INDEX.html & main VIEWS.py File
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                'scaffolder/templates/html/root.html', '{}/root.html'.format(templates_path))


def setup_statics(project):
    # Create JS Static structure
    static_path = '{}/static/js'.format(project.get('name'))
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    f = open('{}/app.js'.format(static_path), 'w')
    print >> f, app_static_template.render()
    f.close()

    f = open('{}/services.js'.format(static_path), 'w')
    print >> f, services_static_template.render(apps=apps)
    f.close()

    f = open('{}/controllers.js'.format(static_path), 'w')
    print >> f, controllers_static_template.render(apps=apps)
    f.close()

    # Create Less Static structure
    less_static_path = '{}/static/less'.format(project.get('name'))
    if not os.path.exists(less_static_path):
        os.makedirs(less_static_path)

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                'scaffolder/templates/static/less/styles.less', '{}/styles.less'.format(less_static_path))

    # Create Partials Static structure
    angular_templates_path = '{}/static/partials'.format(project.get('name'))
    if not os.path.exists(angular_templates_path):
        os.makedirs(angular_templates_path)

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' +
                'scaffolder/templates/static/partials/home.html', '{}/home.html'.format(angular_templates_path))


def setup_main_django_app(project):
    # Connect the different applications with the main URLS.py File
    f = open('{}/urls.py'.format(project.get('name')), 'w')
    print >> f, main_urls_template.render(apps=apps)
    f.close()

    f = open('{}/views.py'.format(project.get('name')), 'w')
    print >> f, main_views_template.render(apps=apps)
    f.close()

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


def setup_django_apps(apps):
    for app in apps:
        call(["python", "manage.py", 'startapp', app.get('name')])

        # Create Template structure
        templates_path = '{}/templates'.format(app.get('name'))
        if not os.path.exists(templates_path):
            os.makedirs(templates_path)

        # Create Static structure
        static_path = '{}/static'.format(app.get('name'))
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        f = open('{}/models.py'.format(app.get('name')), 'w')
        print >> f, models_template.render(app=app)
        f.close()

        f = open('{}/urls.py'.format(app.get('name')), 'w')
        print >> f, urls_template.render(app=app)
        f.close()

        f = open('{}/api.py'.format(app.get('name')), 'w')
        print >> f, api_template.render(app=app)
        f.close()

        f = open('{}/admin.py'.format(app.get('name')), 'w')
        print >> f, admin_template.render(models=app.get('models'))
        f.close()

        # f = open('{}/tests.py'.format(app.get('name')), 'w')
        # print >> f, tests_template.render(app=app)
        # f.close()

if __name__ == '__main__':
    # Load Configuration
    config = yaml.load(file('config.example.yml', 'r'))
    project = config.get('project')
    apps = project.get('apps')

    # Create Jinja2 Environment
    env = Environment(loader=PackageLoader('scaffolder', 'templates'))

    # Load Templates

    # Django
    models_template = env.get_template('django/models.py')
    main_urls_template = env.get_template('django/main_urls.py')
    main_views_template = env.get_template('django/main_views.py')
    urls_template = env.get_template('django/urls.py')
    api_template = env.get_template('django/api.py')
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
    print "************************************************************************************"
    print "* Welcome to the CRUD Wizard v0.1"
    print "************************************************************************************"
    print "Configuring Django 1.10, Angular 1.5.8 and Angular Material 1.1.0!"
    print "0) Removing previous project (if exists)"

    if os.path.exists('{}'.format(project.get('name'))):
        shutil.rmtree('{}'.format(project.get('name')))

    print "1) Creating {} Project...".format(project.get('name'))
    call(["django-admin", "startproject", project.get('name')])

    print "2) Setting up configuration..."
    # Go inside the project.
    os.chdir(project.get('name'))

    setup_global_project_conf(project)
    setup_templates(project)
    setup_statics(project)
    setup_django_apps(apps)
    setup_main_django_app(project)

    # Go back to the parent directory
    os.chdir('../')
    print "Done! In order to complete the configuration please follow the following steps:"
    print "1) Make sure that the models have been properly generated"
    print "2) If so, create migrations by running 'python manage.py makemigrations'"
    print "3) Apply migrations by running 'python manage.py migrate'"
    print "4) Create a superuser using 'python manage.py shell'"
    print "5) Install dependencies by running 'pip install -r requirements.txt'"
    print "6) Enjoy!"

