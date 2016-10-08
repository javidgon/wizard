#!/bin/bash

sudo apt-get update
sudo apt-get install -y tar git curl nano wget dialog net-tools build-essential python-setuptools python-dev libpq-dev postgresql postgresql-contrib
sudo easy_install pip
sudo pip install -r /vagrant/requirements.txt