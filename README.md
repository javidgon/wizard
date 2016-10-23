# Wizard: Angular.js &amp; Django Scaffolding Tool

## 1) Introduction
Let's face it, **nobody likes to create the same CRUD App Skeleton for each new Project**, it takes simply too much time to start off a new prototype... We are not talking only the time consumed creating the `models`, but also the `routing`, `views`, `controllers`, `api`, `tests`, `settings`... It's even worse when you have to connect a Frontend Framework (e.g `Angular.js`) with a Backend (e.g `Django`) for configuring API endpoints. Several hours can be wasted (if you are lucky) only to make them play nicely with each other.

`Wizard` comes to fill this gap. It configures in a few seconds a `Django 1.10` project with pre-configured integration with `Angular 1.5.8`. Meaning, both frameworks will work smoothly with each other, **so you can focus solely on your application logic**.

## 2) Features

* Full Django Backend (including Models) and Frontend glue with Angular.js in a few seconds.
* Basic Django User Token Authentication system configured by default.
* Angular.js framework configuration automatically tailored to work with Django smoothly. 
* `Automatic Generation Rules` system so models can be defined and created automatically based on a `.yml` file.

## 3) How to get started 
You just need to create a `config.yml` file with some configuration (following `Automatic Generation Rules`, please see next Sections) and `Wizard` will do the rest for you.

E.g `config.yml`:

```yml
project:
  name: example # Your Project name
  deployable_in_heroku: True # Do you plan to deploy to Heroku? If so, Wizard will add some settings to make it easier
  apps: # List of Django apps
    - name: account
      models: # List of the models defined for that app
        - name: Member
          unicode:
            - user.email
            - access_level
          fields:
            - user:
              - foreign # Field type
              - notnull # Parameter 
            - access_level:
              - char # Field type
              - notnull # Parameter
            - created_at:
              - datetime
              - auto_now_add
    - name: location
      models:
        - name: City
          unicode:
          - name
          - country
          fields:
            - name:
              - char
              - unique
              - notnull
            - population:
              - int
              - notnull
            - country:
              - char
              - notnull
        - name: Campus
          unicode:
          - name
          - city
          fields:
            - name:
              - char
              - unique
              - notnull
            - rating:
              - char
            - city:
              - foreign
              - notnull
```

Will be transformed in a complete Django Backend (`models.py`, `api.py`, `urls.py`, `views.py`... per application). It simply works.
At the same time it generates a Full CRUD REST API (Create, Read, Update and Delete) for each model!

e.g `urls.py`
```
app_name = 'account'
urlpatterns = [

    url(r'^members/$', MemberApi.as_view(), name='members-list'),
    url(r'^members/(?P<member_id>[0-9]+)/$',
        MemberApi.as_view(), name='members-detail'),
]
```

e.g `api.py`

```
class MemberApi(View):
    def get(self, request, member_id=None, *args, **kwargs):
	...

    def post(self, request, member_id=None, *args, **kwargs):
	...

    def put(self, request, member_id=None, *args, **kwargs):
	...

    def delete(self, request, member_id=None, *args, **kwargs):
	...
```
## 2) Installation & Use

* 1) `git clone https://github.com/javidgon/wizard.git`
* 2) `pip install -r requirements.txt`
* 3) Create a `config.yml` file (You can rename the `config.example.yml` file if you want)
* 4) `cd wizard && python scaffold.py`

## 3) Automatic Model Generation Options available.
As we saw in the first section, it's possible to generate the models (and the full Django backend) based on a `.yml` configuration file. Please use the following rules to set the `Field` type and all its `Parameters`.

#### Fields' Generation Rules

* `char` --> `CharField`
* `text` --> `TextField`
* `url` --> `URLField`
* `int` --> `IntegerField`
* `float` --> `FloatField`
* `date` --> `DateField`
* `datetime` --> `DatetimeField`
* `email` --> `EmailField`
* `boolean` --> `BooleanField`
* `foreign` --> `ForeignKey`
* `manytomany` --> `ManyToManyField`


#### Parameters' Generation Rules

* `unique` --> `unique=True`
* `notunique` --> `unique=False`
* `blank` --> `blank=True`
* `notblank` --> `blank=False`
* `null` --> `null=True`
* `notnull` --> `null=False`
* `auto_now` --> `auto_now=True`
* `auto_now_add` --> `auto_now_add=True`


## 4) Limitations to pay attention to

* It's not intended for Production, only for Prototyping. So only DEV Settings are configured (meaning unsecure).
* It doen't cover a wide range of settings, only the most common ones, so you might need to modify manually some things after the automatic generation (e.g some plurals)
* It doesn't apply migrations. As it's a common practice that a person reviews the models first to see if they have been properly generated.
* It doesn't support ALL `Field` (e.g `JSONField`, `BinaryField`...) in the automatic Django models generation process, only the most common are. Nevertheless, you can always edit them manually afterwards, so it should not be a big problem.
* It doesn't create a full frontend tooling ecosystem (e.g `Grunt`, `Bower`...) as this is not the purpose. But you can add it afterwards of course.

## 5) TODO

* Support proper `pluralization` in jinja2 templates
* Change jinja2 templates interpolation braces
* Improve frontend page (make it nicer)
* Add tests to the resulting Backend project
* Add HTML forms to the resulting Django Backend
* Add automatic Token creation when a User is created
* Add Automatic generation for 'choices' parameters

## 6) LICENSE

MIT
