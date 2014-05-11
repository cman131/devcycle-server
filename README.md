TourTrak Data Collection Server
===============
The server component to the TourTrak system built using Django.

![screenshot](https://raw.githubusercontent.com/tofferrosen/devcycle-server/master/preview.png)

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

## Install PostGIS

1. Install postgreSQL. Refer to official documentation. After, install postGIS, which is a postgreSQL extention for handling spatial data by doing `apt-get install postgresql-9.1-postgis`
2. Setup the postgreSQL database:

* switch to the default postgresql user by running `su postgres`
* create a user w/ read and write permissions: `createuser --pwprompt`
* Create the DCS database used to collect rider information: `createdb DCS`
* Setup the postGIS functions:

```
  psql -d DCS -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
  psql -d DCS -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
  
```

##Installation

* Clone this repository into /usr/local/
* Inside the root directory of our application, install all project dependencies by runnning our setup script `bash setup.sh`
* Create a virtual host & WSGI file for the Apache server to display the Django application. Open the httpd.conf file 'nano /etc/apache2/httpd.conf'. Copy and paste the following, you may edit 
these values if desired (such as where to collect static files).

```
WSGIPythonPath usr/local/devcycle

<VirtualHost *:80>
        ServerName devcycle.se.rit.edu
        ServerAlias devcycle.se.rit.edu
        ServerAdmin someaddress@example.com

        Alias /static /var/www/static/

        <Directory /public/static/>
                Order allow,deny
                Allow from all
        </Directory>

        WSGIDaemonProcess devcycle processes=2 threads=15 display-name=%{GROUP} python-path=/usr/local/devcycle/
        WSGIProcessGroup devcycle
        WSGIScriptAlias / /usr/local/devcycle-server/dataCollection/wsgi.py

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

Set DEBUG to False
Under DATABASES, modify USER and PASSWORD fields to reflect user created in SETUP (above).
HOST should be localhost.
STATIC_ROOT to point to '/var/www/static' unless you modified where to collect these in 
step 6.
SECRET_KEY is a string of at least 32 random characters
KEY to a random string of hex characters a multiple of 16 long
SECRET to a random string of numeric characters a multiple of 16
STATIC_URL = '/static/'
STATICFILES_DIRS = (
  '‘/usr/local/devcycle-server/tour_config/static/’
  )
  
Restart the apache server to put all changes into effect. 

```
/etc/init.d/apache2 reload
```

* Migrate the database scheme using South

TODO.

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


##Configure the Analysis Dashboard
1. Edit the settings file in '/usr/local/devcycle/dataCollections/settings.py'

* TIME_ZONE to reflect the timezone of the server in “tz database” format (e.g. ‘America/New_York’)
* DEFAULT_MAP_LAT and DEFAULT_MAP_LON to the latitude and longitude, respectively, that maps in the dashboard should default to.
* MAP_TILE_SERVER to the hostname of the server to retrieve map tiles from - currently configured to use MapQuest's free OSM tile server hosting.



