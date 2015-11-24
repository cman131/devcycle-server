TourTrak Data Collection Server
===============
The server component to the TourTrak system built using Django on **Ubuntu 14.04**.

![screenshot](https://raw.githubusercontent.com/tofferrosen/devcycle-server/master/preview.png)

###Dependencies
**Note:** These will be installed by a script in the Installation instructions below

* Python 2.7
* Pip for Python2
* python-django version 1.6.11
* apache server
* mod_wsgi
* postgresQL
* PostGIS
* postgresql-server-9.3
* psycopg2
* binutils
* gdal-bin
* libproj-dev
* memcached
* rabbitmq-server


## Install Postgres with PostGIS (Install The Database)

_(This is where you begin the server setup instructions)_

1. Update aptitude

	`sudo apt-get update`
2. Install postgreSQL

	`sudo apt-get install postgresql`
3. After, install postGIS, which is a postgreSQL extention for handling spatial data

	`sudo apt-get install postgresql-9.3-postgis-2.1`
4. Setup the postgreSQL database:

* switch to the default postgresql user by running

	`sudo -iu postgres`
* create a user w/ read and write permissions:

	`createuser --pwprompt dev`
	
	 - _**Note:** Change "dev" to what you want the database username to be_
	 - _**Note:** The password cannot be blank_
* Create the DCS database used to collect rider information:

	`createdb DCS`
* Setup the postGIS functions:

```
  psql DCS
  CREATE EXTENSION postgis;
  CREATE EXTENSION postgis_topology;
  \q
```
* Sign out of postgresuser

    `exit`

##Install The Application

1. Install git

	`sudo apt-get install git`
2. Create a 'devcycle' directory in /usr/local/

	`sudo mkdir /usr/local/devcycle`
3. Clone this repository into /usr/local/devcycle
 
	`sudo git clone https://github.com/tourtrak/devcycle-server.git /usr/local/devcycle`
4. **IMPORTANT:** The directory must be named 'devcycle' and not 'devcycle-server'. Django does not support hyphen names for it's applications.</b>
5. Inside the root directory of your application, install all project dependencies by running our setup script

	`cd /usr/local/devcycle`

	`sudo bash setup.sh` _(This will take a significant amount of time on mod_wsgi-httpd, 10-20 mins)_
6. Create a virtual host & WSGI file for the Apache server to display the Django application by creating a new .conf file from the template.

 ```
sudo cp /usr/local/devcycle/001-devcycle.conf.template /etc/apache2/sites-available/001-devcycle.conf
sudo vim /etc/apache2/sites-available/001-devcycle.conf
 ```
 * Change "SERVER_NAME" to match your server's name ex: `devcycle`
 * Change "SERVER_ADDRESS" to match your domain ex: `devcycle.se.rit.edu`
 * Change "SERVER_EMAIL_ADDRESS" to match your email address ex: `pandaman@example.com`
 * Change "DEBUG" to `True` if you are *not* in production
 * Change "TIME_ZONE" to match the timezone of the server in “tz database” format (e.g. ‘America/New_York’)
 * Change "DEFAULT_MAP_LAT" and "DEFAULT_MAP_LON" to match the latitude and longitude, respectively, that maps in the dashboard should default to.
 * Change "MAP_TILE_SERVER" to match the hostname of the server to retrieve map tiles from (currently configured to use MapQuest's free OSM tile server)

7. Create and Change the application settings:

 ```
sudo cp /usr/local/devcycle/dataCollection/settings.py.template /usr/local/devcycle/dataCollection/settings.py
sudo vim /usr/local/devcycle/dataCollection/settings.py
 ```
 * Under DATABASES, modify USER and PASSWORD fields to reflect the database user you created in ["Install The Database"](#install-postgres-with-postgis-install-the-database).

8. Restart the apache server to put all changes into effect.

 ```
sudo /etc/init.d/apache2 reload
 ```


###Setup The Database
[South](http://south.aeracode.org/) is a schema and data migration tool for Django. It is used for easily
migrating the database schema from database to database if needed. It is also used in the case of making updates
to models then wanting those changes reflected in the database schema. South is already installed if you ran the `bash setup.sh` command. Recommend looking at the docs for more information [docs](http://south.readthedocs.org/en/latest/index.html)

At this point the database schema for the Server does not exist yet. We will use South to add it. South will look at the current models to set-up the schema that the Server requires.

*Note all commands below need to be ran within the root directory of the Django Project (/usr/local/devcycle)*

This command will create the migrations:

`sudo python manage.py syncdb --all`

 - _**Note:** this may prompt you to create a django auth user. Follow that process as well if it does._

Restart server again.

```
sudo service apache2 reload
```

* Import all static files.

```
sudo python manage.py collectstatic
```

Restart server again:

```
sudo service apache2 reload
```


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

### Configs and JSON files

Configs are formatted as follows:
```
URL (the connection URL)
#Requests (max 200)
JSON (the name of the JSON object to pull data from)
- (terminates the test definition)
```

Example config:
```
http://centri-pedal2.se.rit.edu/join_group/groupCode/riderId/
200
join_group.json
-
```
Main_GET.rb allows for groupCode and riderId to be specified as hooks in the URL for data to be plugged into dynamically.

A corresponding JSON object would then look like this:
```
{
	"groupCode" : "BIG1",
	"riderId" : 15
}
```

You can also use random test data by specifying the groupCode or riderId to be "random". Here is an example JSON for a randomized test:
```
{
	"groupCode" : "random",
	"groupCodeBase" : "BIG",
	"groupCodeMin" : 1,
	"groupCodeMax" : 50,
	"riderId" : "random",
	"riderIdMin" : 2,
	"riderIdMax" : 100
}
```

Random group codes are generated by combing a groupCodeBase ("BIG" in the above example) with a random number. The above JSON would result in a random selection between BIG1, BIG2, BIG3, ..., BIG50.

Random rider IDs are selected from the specified range of values.

### Recording and Analyzing

To look at the Server performance in real time the linux command `top` is used. When running
the load tests it is important to record the performance of the server. When you run the
load test make sure you run top on the server simultaneously in order to record the
performance of the server at the time of the tests. By using this command and
piping the results this is achievable to analyze the data. Then after recording,
grep the text in order to get the parameters you want then simply graph the numbers.

The command below pipes the top command every 1 second into a text file called example.
`top -b -d 1 > example.txt`

The command below then greps for only the CPU performance numbers
`cat example.txt | grep Mem | cut -c 8-53 | nl -i 1`

The command below then greps for only the Mem performance numbers
`cat example.txt | grep Cpu | cut -c 35-39 | nl -i 1`

### Errors

You may encounter an error about a missing libcurl.dll when you attempt to run the load testing framework. Follow these steps to resolve it:

Go to this URL: http://rubyinstaller.org/downloads/

Download DevKit-tdm-32-4.5.2-20111229-1559-sfx.exe

Follow these instructions to set the devkit up on your machine: https://github.com/oneclick/rubyinstaller/wiki/Development-Kit

Go to this URL: http://www.paehl.com/open_source/?CURL_7.39.0&PHPSESSID=b155d4a69c7aa26b1fd67e7201d4fb3e

Select "Download libcurl.dll (all versions) only"

Extract the contents of the archive, copy libcurl.dll from the SSL folder, and paste it into your Ruby /bin folder (probably C:\Ruby193\bin if you're on Windows)


# Tips
## Postgres Database Commands
#####Connecting to the database after setup
1. Type `sudo -iu postgres`
2. Type `psql DCS`

#####Some helpful commands include:
1. `\dt` to list all tables
2. `\q` to quit
3. `psql DCS < /path/to/script/script.sql` for running scripts without having to connect

## Creating Migrations
When you make changes to the model, you need to create migrations to reflect the
changes in the database. You can do so by running this command:

`sudo python manage.py schemamigration MODEL_NAME NAME_OF_MIGRATION --auto`

* change "MODEL_NAME" to the model you changed ex: "rider"
* change "NAME_OF_MIGRATION" to what you want to call it.

These commands will then apply the newly created migrations to the database:

`sudo python manage.py migrate rider 0001`

`sudo python manage.py migrate location_update 0001`

`sudo python manage.py migrate tour_config 0001`

Now you need to reload the server

```
sudo service apache2 reload
```
