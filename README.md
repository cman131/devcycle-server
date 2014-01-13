TourTrak Data Collection Server
===============
The server component to the TourTrak system built using Django.

###Dependencies
* Python 2.7
* Pip for Python
* python-django
* apache server
* mod_wsgi
* postgresQL
* PostGIS
* postgresql-server-dev-9.1
* psycopg2
* binutils
* gdal-bin
* libproj-dev
* memcached
* rabbitmq-server

##Setup

1. Install pip `apt-get install python pip`, and then upgrade: `pip install --upgrade pip`
2. Install Django `pip install python-django`
3. Install the Apache Server `aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert`
4. Install mod_wsgi `aptitude install libapache2-mod-wsgi`. Then, restart apache server by running: `service apache2 restart`
5. Install postgreSQL. Refer to official documentation. After, install postGIS, which is a 
postgreSQL extention for handling spatial data: `apt-get install postgresql-9.1-postgis`
6. Setup the postgreSQL database:
* switch to the default postgresql user by running `su postgres`
* create a user w/ read and write permissions: `createuser --pwprompt`
* Create the DCS database used to collect rider information: `createdb DCS`
* Setup the postGIS functions:

```
  psql -d DCS -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
  psql -d DCS -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
  
```
Importation of database schema are under Installation instructions. Now your server is ready for the application to be installed.

##Installation

###Install application dependencies
* Install postgreSQL-9.1

```
apt-get update
apt-get install postgresql-9.1
apt-get install postgresql-server-dev-9.1
```

* Install postgresSQL database adapter

```
pip install psycopg2
```

* Install the rest of the dependencies:

```
apt-get install binutils
apt-get install gdal-bin
apt-get install libproj-dev
apt-get install memcached
apt-get install rabbitmq-server
```

* Create a new folder called 'devcycle' under '/usr/local'. Git clone this repo here and stay in this directory.
* Install the required python eggs:

```
pip install distribute
pip install Crypto
pip install Django
pip install Markdown
pip install PyYAML
pip install South
pip install django-filter
pip install django-rest
pip install djangorestframework
pip install mimeparse
pip install pep8
pip install pycrypto
pip install python-dateutil
pip install wsgiref
pip install python-memcached
pip install celery
pip install django-celery
pip install psycopg2
pip install django-admin-bootstrapped
```

* Create a virtual host & WSGI file for the Apache server to display the Django application.
Open the httpd.conf file 'nano /etc/apache2/httpd.conf'. Copy and paste the following, you may edit 
these values if desired (such as where to collect static files).

```
WSGIPythonPath usr/local/devcycle

<VirtualHost *:80>
        ServerName devcycle.se.rit.edu
        ServerAlias devcycle.se.rit.edu
        ServerAdmin cbr4830@rit.edu

        Alias /static /var/www/static/

        <Directory /public/static/>
                Order allow,deny
                Allow from all
        </Directory>

        WSGIDaemonProcess devcycle processes=2 threads=15 display-name=%{GROUP} python-path=/usr/local/devcycle/
        WSGIProcessGroup devcycle
        WSGIScriptAlias / /usr/local/devcycle/dataCollection/wsgi.py

        <Directory /usr/local/devcycle/dataCollection>
                <Files wsgi.py>
                Order deny,allow
                Allow from all
                </Files>
        </Directory>
</VirtualHost>
```

* Change the application settings:

```
nano /usr/local/devcycle/dataCollection/settings.py
```

** Set DEBUG to False
** Under DATABASES, modify USER and PASSWORD fields to reflect user created in SETUP (above).
** HOST should be localhost.
** STATIC_ROOT to point to '/var/www/static' unless you modified where to collect these in 
step 6.
** SECRET_KEY is a string of at least 32 random characters
** KEY to a random string of hex characters a multiple of 16 long
** SECRET to a random string of numeric characters a multiple of 16
** STATIC_URL = '/static/'
** STATICFILES_DIRS = (
  '‘/usr/local/devcycle/tour_config/static/’
  )

* Restart the apache server to put all changes into effect. 

```
etc/init.d/apache2 reload
```

* Migrate the database scheme with the SQL script included.

```
psql DCS < DCS.sql
```

Restart server again.

```
/etc/init.d/apache2 reload
```

* Import all static files.

```
python manage.py collectstatic
```

Restart server again:

```
/etc/init.d/apache2 reload
```

##Install a local OpenStreetMap Tile Server
1. Follow instructions from http://switch2osm.org/serving-tiles/building-a-tile-server-from-packages/

##Install the Analysis Dashboard
1. Edit the settings file in '/usr/local/devcycle/dataCollections/settings.py'

* TIME_ZONE to reflect the timezone of the server in “tz database” format (e.g. ‘America/New_York’)
* GCM_API_KEY to the Google Cloud Messaging API key which should be used to contact users of the Android Application
* DEFAULT_MAP_LAT and DEFAULT_MAP_LON to the latitude and longitude, respectively, that maps in the dashboard should default to.
* MAP_TILE_SERVER to the hostname of the server to retrieve map tiles from, or ‘’ if using a local tile server



