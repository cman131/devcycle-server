#!/usr/bin/ruby

require 'faraday' #http client lib

require 'typhoeus' #parallel http requests WAITING FOR V 0.6.7 for patch current 0.6.6 is buggy this won't work

require 'typhoeus/adapters/faraday' #typhoeus adapter

require 'benchmark' #measurements/stats

require 'json'

require_relative 'constants.rb'

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

#
# Type of Request, Location_update or
# rider registration
@request_type

#
# Loads the config file and parses it.
# After parsing the config file a request
# is then sent to the server. 
#
class Load

    def initialize(request_type,configs)
      @request_type = request_type
      @configs = configs
      @prng  = Random.new
    end#initialize


    def start
      @configs.each do |config|

        url = config[0]
        count = config[1]
        if @request_type < FrameworkConstants::GET_MIN_REQUEST_TYPE then json_path = "jsons/#{config[2]}" end

        @url = url

        @manager = Typhoeus::Hydra.new(max_concurrency: 200) #200 is max limit

        connection = Faraday.new(url: url) do |builder|
          builder.use LoadTestHandler
          builder.adapter :typhoeus
        end#connection loop

        #This parses the json file into a hash
        if @request_type < FrameworkConstants::GET_MIN_REQUEST_TYPE then 
			json = JSON.parse(IO.read(json_path))
        	#Execute parallel requests
        	parallel_posts(connection, count, json)
		else
			parallel_gets(connection, count)
	end


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

    def parallel_gets(conn, count)
	
	conn.in_parallel(@manager) do
		for i in 1..count
			get(conn)
		end
	end
    end

    # Performs the actual post requests
    #
    #
    #
    # @param - connection manager
    # @param - json file
    def post(conn,json)

      if @request_type == FrameworkConstants::LOCATION_UPDATE_REQUEST then json = randomizeLatLong(json) end

      conn.post do |request|

        request.url @url

        request.headers['Content-Type'] = 'application/json'

        request.body = json.to_json

      end#conn.post

    end#post

    def get(conn)


	conn.get do |request|
    @gc = randomGroupCode()
    @r = randomRiderID()

    if @request_type == FrameworkConstants::GET_REQUEST_RGC then request.url @url.concat(@gc + "/" + @r + "/") end
    if @request_type == FrameworkConstants::GET_REQUEST_R then request.url @url.concat(@r + "/") end
    if @request_type == FrameworkConstants::GET_REQUEST_GC then request.url @url.concat(@gc + "/") end
		#request.url @url
	end
    end

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

    end
    # Random Group Code
    def randomGroupCode()
      @randNum = @prng.rand(1...100)
      return "BIG".concat(@randNum.to_s)
    end

    # Random Rider ID
    def randomRiderID()
      return @prng.rand(1...129) 
    end


end#class
