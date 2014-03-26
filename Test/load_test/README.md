#  Devcycle Load Test Framework

This directory contains the Load Test Framework for the Server.
The framework is written in ruby and is command line based.
A configuration file is used to configure the load test(s). Please see
`config_sample.txt` for formatting and usage.

The framework is primairly based on 2 ruby gems, `typhoeus` and
`faraday`. Typhoeus is used for making parallel http requests
to simulate traffic. Faraday is a http wrapper to make it
easier to create http requests.

This can be used to simulate up to 200 concurrent http requests at a single time
based on Typhoeus. To increase that number you must run the framework
simultaneously on multiple machines.

##  SET-UP
1. Framework works for ruby version 1.9.3 have not tested for other versions of ruby.

2. gem install typhoeus

3. gem install faraday

###  Files
/Main.rb - the main file to run the system

framework/load_test.rb - contains most of the logic and processing

jsons/cpu_load.json - location_update request json to send to the server

configs/config_sample.txt - Configuration Sample w/ example format

framework/response_handler.rb - Response Handler for the Http Requests

###  Directory
framework/ - contains the logic of the framework

configs/ - contains all the config files

jsons/ - contains all json files


##  Usage

If you want to write your own configurations then include them in the configs/ directory. If you want
to write your own json then include them in the jsons/ directory. 

It is important to note that you do not need specify the full relative paths
of the config files when running the framework on the command line. The framework
will search for all config files in the configs/ directory. When specifying the json
files in the config files, you do not need to specify the full relative paths
for the json files, just the name of the file. The framework looks automatically
in the jsons/ directory for all json files. 

`ruby Main.rb config_sample.txt`

`./Main.rb config_sample.txt`


