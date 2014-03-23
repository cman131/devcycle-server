#!/usr/bin/ruby

require 'faraday' #http client lib

require 'typhoeus' #parallel http requests WAITING FOR V 0.6.7 for patch current 0.6.6 is buggy this won't work

require 'typhoeus/adapters/faraday' #typhoeus adapter

require 'benchmark' #measurements/stats

require 'json'

require_relative 'response_handler'

#
# Test Configurations
#
@configs

#
# Server URL
#
@url

#
# Typhoeus Hydra Manager for concurrency
#
@manager

#
# Random Number Generator
#
@prng 


class Load_Test

    def initialize(configs)
      @configs = configs
      @prng  = Random.new
    end#initialize


    def start
      @configs.each do |config|

        url = config[0]
        count = config[1]
        json = config[2]

        @url = url

        @manager = Typhoeus::Hydra.new(max_concurrency: 200) #200 is max limit

        connection = Faraday.new(url: url) do |builder|
          builder.use LoadTestHandler
          builder.adapter :typhoeus
        end#connection loop

        #This parses the json file into a hash
        json = JSON.parse(IO.read(json))

        #Testing the body of this
        #json = {a:1}

        #Execute parallel requests
        parallel_posts(connection, count, json)


      end#config loop

    end#start



    private

    # Performs the parallel post requests
    #
    #
    #
    # @param - connection manager
    # @param - iteration count
    # @param - json file
    def parallel_posts(conn, count, json)

      conn.in_parallel(@manager) do

        for i in 1..count

          post(conn,json)

        end#loop

      end#connection

    end#parallel_posts


    # Performs the actual post requests
    #
    #
    #
    # @param - connection manager
    # @param - json file
    def post(conn,json)

      json = randomizeLatLong(json)

     conn.post do |request|

        request.url @url

        request.headers['Content-Type'] = 'application/json'

        request.body = json.to_json

      end#conn.post

    end#post

    #
    # Simulate a moving biker
    # by randomizing movement
    # by altering the latitude
    # and longitude. Algorithm
    # actually randomly moves
    # biker
    #
    # @param - json hash
    # @return - new json hash
    def randomizeLatLong(json)

      #Get the locations array
      loc_arr = json["locations"]
      
      #iterate through each loc
      loc_arr.each do |loc|

        #randomize +/- of random number
        lat_sign = @prng.rand(0...2)
        long_sign = @prng.rand(0...2)

        #randomize the value to lat & long
        lat_val = @prng.rand(0.0...10.0)
        long_val = @prng.rand(0.0...10.0)

        #change position here
        if lat_sign == 0 then loc["latitude"] -= lat_val else loc["latitude"] += lat_val end
        if long_sign == 0 then loc["longitude"] -= long_val else loc["longitude"] += long_val end

      end#loop

      return json

    end#randomizeLatLong


end#class
