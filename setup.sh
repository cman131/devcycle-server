#!/bin/bash
# setup.sh for configuring Ubuntu 12.04 LTS EC2 instance with the 
# devcycle django server installed. easy and quick way to install
# all the required dependencies.

# Install necessary dependencies
sudo apt-get update
sudo apt-get install git --yes
sudo apt-get install python2 --yes
sudo apt-get install python-pip --yes
sudo apt-get install python-dev --yes
sudo apt-get install build-essential --yes
sudo pip install --upgrade pip
sudo apt-get install binutils --yes
sudo apt-get install gdal-bin --yes
sudo apt-get install libproj-dev --yes
sudo apt-get install memcached --yes
sudo apt-get install rabbitmq-server --yes
sudo apt-get install postgresql --yes
sudo apt-get install python-psycopg2 --yes
sudo apt-get install python-gobject --yes
sudo apt-get install python-pycurl --yes
sudo apt-get install postgresql-9.3-postgis-2.1 --yes
sudo apt-get install landscape-client --yes

# Install the Apache server
sudo apt-get install apache2 --yes
sudo apt-get install apache2-mpm-prefork --yes
sudo apt-get install apache2-utils --yes
sudo apt-get install libexpat1 --yes
sudo apt-get install ssl-cert --yes
sudo apt-get install apache2-dev --yes

# Install mod_wsgi
sudo apt-get install libapache2-mod-wsgi --yes
sudo service apache2 restart

# Install the required python eggs
sudo pip install -r /usr/local/devcycle/requirements.txt
