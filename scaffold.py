from jinja2 import Environment, PackageLoader
from subprocess import call
import yaml
import os
import shutil

# Load Configuration
config = yaml.load(file('config.yml', 'r'))
project = config.get('project')
apps = project.get('apps')

# Create Jinja2 Environment
env = Environment(loader=PackageLoader('scaffolder', 'templates'))

# Load Templates
models_template = env.get_template('models.py')
main_urls_template = env.get_template('main_urls.py')
urls_template = env.get_template('urls.py')
api_template = env.get_template('api.py')

# Start Scaffolding

print "0) Removing previous project (if it exists)"
shutil.rmtree('{}'.format(project.get('name')))

print "1) Creating {} Project...".format(project.get('name'))
call(["django-admin", "startproject", project.get('name')])


print "2) Setting up applications..."
# Go inside the project.
os.chdir(project.get('name'))
# Connect the different applications with the main URLS.py File
f = open('{}/urls.py'.format(project.get('name')), 'w')
print >> f, main_urls_template.render(apps=apps)
f.close()

for app in apps:
    call(["python", "manage.py", 'startapp', app.get('name')])

    f = open('{}/models.py'.format(app.get('name')), 'w')
    print >> f, models_template.render(models=app.get('models'))
    f.close()

    f = open('{}/urls.py'.format(app.get('name')), 'w')
    print >> f, urls_template.render(app=app)
    f.close()

    f = open('{}/api.py'.format(app.get('name')), 'w')
    print >> f, api_template.render(app=app)
    f.close()

# Add added applications to the SETTINGS.py file

new_settings_file = ''
for line in open("{}/settings.py".format(project.get('name'))).readlines():
    new_settings_file += line
    if line.startswith("INSTALLED_APPS = ["):
        for app in apps:
            new_settings_file += "    '{}.apps.{}Config',\n".format(
                app.get('name'), app.get('name').capitalize())

f = open('{}/settings.py'.format(project.get('name')), 'w')
print >> f, new_settings_file
f.close()

# Go back to the parent directory.
os.chdir('../')
print "Done!"

