# Wizard: Angular.js &amp; Django Scaffolding Tool

## 1) Introduction
Let's face it, nobody likes to create the same old App Skeleton everytime you want to start off a new Prototype. It's even worse
when you have to connect a Frontend Framework (e.g `Angular.js`) with a Backend (e.g `Django`). Several hours can be wasted if you are lucky, otherwise it could be days.

`Wizard` comes to fill this gap. You can create a Angular.js(1.5.8) & Django(1.10) skeleton in minutes, including DB Models! You just need to create a `config.yml` file with some configuration and `Wizard` will do the rest for you.

`config.yml`:

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
            - surname:
              - char
              - notnull
            - age:
              - int
            - created_at:
              - datetime
              - auto_now_add
            - last_login:
              - datetime
              - auto_now
        - name: Admin
          str:
            - user
            - access_level
          fields:
            - user:
              - foreign
              - notnull
            - rights:
              - char
            - access_level:
              - int
              - notnull
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
        - name: Room
          str:
          - name
          - campus
          fields:
            - name:
              - char
              - unique
              - notnull
            - floor:
              - int
              - notnull
            - campus:
              - foreign
              - notnull
```

Will be transformed in several fully working `models.py`, `api.py`, `urls.py`, `views.py`... files per each application. It simply works.
At the same time it generates a Full REST API for each model! And configures the frontend to easily connect to it.

```
├── account
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── myproject
│   ├── __init__.py
│   ├── settings.py
│   ├── static
│   │   ├── app.js
│   │   ├── controllers.js
│   │   └── services.js
│   ├── templates
│   │   └── index.html
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
├── location
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── Procfile
└── requirements.txt
```

## 2) Installation & Use

* 1) `git clone https://github.com/javidgon/wizard.git`
* 2) `pip install -r requirements.txt`
* 3) Create `config.yml` (You can use `config.example.yml` if you rename it)
* 4) `cd wizard && python scaffold.py`

## 3) What does it not do?

* It's not intended for Production, only for Prototyping. So only DEV Settings are configured (meaning unsecure).
* It doesn't set up an Authentication system by default.
* It doesn't apply migrations. As it's strongly recommended that a person reviews the models before to see if they have been properly generated.
* It doesn't support complex Field parameters in Django models. Only the most common parameters are supported. You can always edit them manually, so no problem there.
* It doesn't create a full frontend tooling ecosystem (e.g `Grunt`, `Bower`...) as this is not the purpose. But you can add it afterwards of course.

## 4) TODO

* Support proper `pluralization` in jinja2 templates
* Create a routing system inside Angular.js frontend
* Improve frontend page (make it nicer)
* Finish Heroku integration
* Structure better the `scaffold.py` file
* Add tests to the resulting Backend project

## 5) LICENSE

MIT