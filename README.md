TourTrak Data Collection Server
===============
The server component to the TourTrak system built using Django on an <b>Ubuntu 12.04</b> Server.

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
* Inside the root directory of your application, install all project dependencies by runnning our setup script `bash setup.sh`
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

###Migrate the Database Schema using South
[South](http://south.aeracode.org/) is a schema and data migration tool for Django. It is used for easily
migrating the database schema from database to database if needed. It is also used in the case of making updates
to models then wanting those changes reflected in the database schema. South is already installed if you ran the `bash setup.sh` command. Recommend looking at the docs for more information [docs](http://south.readthedocs.org/en/latest/index.html)

At this point the database schema for the Server does not exist yet. We will use South to add it. South will look at the current models to set-up the schema that the Server requires. 

*Note all commands below need to be ran within the root directory of the Django Project*

1. Need to load the South table into the database, this is where all the migration instructions are kept. *--all* make sures South is tracking all tables already set. 

`./manage.py syncdb --all`

2. The models already exist and are initialized by South already, we need to track it. They are stored in the migrations folder of each model.

* `./manage.py migrate rider 0001 --fake` 

* `./manage.py migrate location_update 0001 --fake` 

* `./manage.py migrate tour_config 0001 --fake` 

This should add the current models to the database. 

After making changes to models and wanting to reflect changes in db. 

Check if changes were made to the model:

`./manage.py schemamigration <model_name> --auto`

2. Execute the changes:

`./manage.py migrate <model_name>`

When adding models

`./manage.py schemamigration <model_name> --initial`








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

##Devcycle Load Test Framework

The following refers to the Load Test Framework for the Server.
The framework is written in ruby and is command line based.
A configuration file is used to configure the load test(s). Please see
`config_sample.txt` for formatting and usage.

The framework is primairly based on 2 ruby gems, [typhoeus](http://typhoeus.github.io/) and
[faraday](https://github.com/lostisland/faraday). Typhoeus is used for making parallel http requests
to simulate traffic. Faraday is a http wrapper to make it
easier to create http requests.

This can be used to simulate up to 200 concurrent http requests at a single time
based on Typhoeus. To increase that number you must run the framework
simultaneously on multiple machines.

###  SET-UP

*Framework works for ruby version 1.9.3 have not tested for other versions of ruby.*

1. `gem install typhoeus`

2. `gem install faraday`

###  Files

/Main.rb - the main file to run the system

framework/load_test.rb - contains most of the logic and processing

jsons/cpu_load.json - location_update request json to send to the server

configs/config_sample.txt - Configuration Sample w/ example format

framework/response_handler.rb - Response Handler for the Http Requests

###  Directory

framework/ - contains the logic of the framework

configs/ - contains all the config files

jsons/ - contains all json files. The json files constitute the data you are sending. You specify which json file in the config file


###  Usage

If you want to write your own configurations then include them in the configs/ directory. If you want
to write your own json then include them in the jsons/ directory. 

It is important to note that you do not need specify the full relative paths
of the config files when running the framework on the command line. The framework
will search for all config files in the configs/ directory. When specifying the json
files in the config files, you do not need to specify the full relative paths
for the json files, just the name of the file. The framework looks automatically
in the jsons/ directory for all json files. 

Sample command

`ruby Main.rb config_sample.txt`

or

`./Main.rb config_sample.txt`


### Recording and Analyzing

To look at the Server performance in real time the linux command `top` is used. When running
the load tests it is important to record the performance of the server. When you run the
load test make sure you run top on the server simultaneously in order to record the
performance of the server at the time of the tests. By using this command and
pipping the results this is achievable to analyze the data. Then after recording, 
grep the text in order to get the parameters you want then simply graph the numbers. 

The command below pipes the top command every 1 second into a text file called example.
`top -b -d 1 > example.txt`

The command below then greps for only the CPU performance numbers
`cat example.txt | grep Mem | cut -c 8-53 | nl -i 1`

The command below then greps for only the Mem performance numbers
`cat example.txt | grep Cpu | cut -c 35-39 | nl -i 1`



