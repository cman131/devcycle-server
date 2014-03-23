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

##  Files
/Main.rb - the main file to run the system

/load_test.rb - contains most of the logic and processing

/location_update.json - location_update request json to send to the server

/config_sample.txt - Configuration Sample w/ example format

/response_handler.rb - Response Handler for the Http Requests


##  Usage

`ruby Main.rb config_sample.txt`

`./Main.rb config_sample.txt`

