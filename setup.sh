#!/bin/bash
# setup.sh for configuring Ubuntu 12.04 LTS EC2 instance with the 
# devcycle django server installed. easy and quick way to install
# all the required dependencies.

# Install necessary dependencies
sudo apt-get update
sudo apt-get install python2 python-pip python-dev build-essential 
sudo pip install --upgrade pip 
sudo apt-get install git
sudo apt-get install binutils
sudo apt-get install gdal-bin
sudo apt-get install libproj-dev
sudo apt-get install memcached
sudo apt-get install rabbitmq-server
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install postgresql-9.3-postgis-2.1

# Install the Apache server
sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert apache2-dev

# Install mod_wsgi
sudo aptitude install libapache2-mod-wsgi
sudo service apache2 restart

# Install the required python eggs
sudo pip install -r /usr/local/devcycle/requirements.txt

sudo chmod 777 /var/www/django-logs/default.log
