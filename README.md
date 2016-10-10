# Wizard: Angular.js &amp; Django Scaffolding Tool

## 1) Introduction
Let's face it, **nobody likes to create the same CRUD App Skeleton for each new Prototype**. It's even worse when you have to connect a Frontend Framework (e.g `Angular.js`) with a Backend (e.g `Django`) for configuring API stuff. Several hours can be wasted if you are lucky, otherwise it could be days.

`Wizard` comes to fill this gap. It configures in a few seconds the following CRUD Stack (including statics' tools and DB Models!), so you can focus solely on your application logic:
 
 * 1) Angular 1.5.8
 * 2) Angular Material 1.1.0
 * 3) Django 1.10
 * 4) Less.js

You just need to create a `config.example.yml` file with some configuration (following `Automatic Generation Rules`, please see next Sections) and `Wizard` will do the rest for you.

E.g `config.example.yml`:

```yml
project:
  name: example
  deployable_in_heroku: True
  apps:
    - name: account
      models:
        - name: User
          str:
            - name
            - surname
          fields:
            - name:
              - char
              - notnull
            - email:
              - email
              - unique
              - notnull
            - created_at:
              - datetime
              - auto_now_add
    - name: location
      models:
        - name: City
          str:
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
          str:
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
At the same time it generates a Full CRUD REST API (Create, Read, Update and Delete) for each model! And configures Angular.js to easily access to them using Services.

```
├── account
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── example
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── settings.py
│   ├── settings.pyc
│   ├── static
│   │   ├── js
│   │   │   ├── app.js
│   │   │   ├── controllers.js
│   │   │   └── services.js
│   │   ├── less
│   │   │   └── styles.less
│   │   └── partials
│   │       └── home.html
│   ├── templates
│   │   └── root.html
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── location
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── requirements.txt
```

## 2) Installation & Use

* 1) `git clone https://github.com/javidgon/wizard.git`
* 2) `pip install -r requirements.txt`
* 3) Create `config.example.yml` (You rename `config.example.yml` if you want)
* 4) `cd wizard && python scaffold.py`

## 3) Automatic Model Generation Options available.
As we saw in the first section, it's possible to generate the models (and the full Django backend) based on a `.yml` configuration file. Please use the following rules to set the `Field` type and all its `Parameters`.

#### Fields' Generation Rules

* `char` --> `CharField`
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


## 4) What does it not do?

* It's not intended for Production, only for Prototyping. So only DEV Settings are configured (meaning unsecure).
* It doesn't set up an Authentication system by default.
* It doesn't apply migrations. As it's strongly recommended that a person reviews the models before to see if they have been properly generated.
* It doesn't support complex Field parameters in Django models. Only the most common parameters are supported. You can always edit them manually, so no problem there.
* It doesn't create a full frontend tooling ecosystem (e.g `Grunt`, `Bower`...) as this is not the purpose. But you can add it afterwards of course.

## 5) TODO

* Support proper `pluralization` in jinja2 templates
* Improve frontend page (make it nicer)
* Add tests to the resulting Backend project

## 6) LICENSE

MIT