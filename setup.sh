#!/bin/bash
# setup.sh for configuring Ubuntu 12.04 LTS EC2 instance with the 
# devcycle django server installed. easy and quick way to install
# all the required dependencies.
#
# note: this does not install postgresql and the subsequent database
# necessary. this was setup used '13/'14 using an EC2 instance with Amazon RDS
# running postgresql with the postgis extentions.

# Install necessary dependencies
sudo apt-get install python-pip python-dev build-essential 
sudo pip install --upgrade pip 
sudo apt-get install python-django
sudo apt-get install binutils
sudo apt-get install gdal-bin
sudo apt-get install libproj-dev
sudo apt-get install memcached
sudo apt-get install rabbitmq-server
sudo apt-get update
sudo apt-get install postgresql-9.1
sudo apt-get install postgresql-server-dev-9.1

# Install the Apache server
sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

# Install mod_wsgi
sudo aptitude install libapache2-mod-wsgi
sudo service apache2 restart

# Install the required python eggs
sudo pip install distribute
sudo pip install Crypto
sudo pip install Django
sudo pip install Markdown
sudo pip install PyYAML
sudo pip install South
sudo pip install django-filter
sudo pip install django-rest
sudo pip install djangorestframework
sudo pip install mimeparse
sudo pip install pep8
sudo pip install pycrypto
sudo pip install python-dateutil
sudo pip install wsgiref
sudo pip install python-memcached
sudo pip install celery
sudo pip install django-celery
sudo pip install psycopg2
sudo pip install django-admin-bootstrapped

