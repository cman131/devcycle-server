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
class Load_GET

    def initialize(request_type,configs)
      @request_type = request_type
      @configs = configs
      @prng  = Random.new
    end#initialize


    def start
      @configs.each do |config|

        url = config[0]
        count = config[1]
        json_path = "jsons/#{config[2]}"

        @url = url

        @manager = Typhoeus::Hydra.new(max_concurrency: 200) #200 is max limit

        connection = Faraday.new(url: url) do |builder|
          builder.use LoadTestHandler
          builder.adapter :typhoeus
        end#connection loop

        #This parses the json file into a hash
        json = JSON.parse(IO.read(json_path))

        #Execute parallel requests
        parallel_gets(connection, count, json)


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
    def parallel_gets(conn, count, json)

      conn.in_parallel(@manager) do

        for i in 1..count

          get(conn,json)

        end#loop

      end#connection

    end#parallel_posts


    # Performs the actual post requests
    #
    #
    #
    # @param - connection manager
    # @param - json file
    def get(conn,json)

      #if @request_type == FrameworkConstants::LOCATION_UPDATE_REQUEST then json = randomizeLatLong(json) end

      conn.get do |request|

        request.url make_url(@url, json)

        #request.headers['Content-Type'] = 'application/json'

        #request.body = json.to_json

      end#conn.post

    end#post
	
	def make_url(url, json)
		retstr = url.dup
		if retstr.strip.match(/groupCode/) != nil
				code = get_group_code(json)
				retstr = retstr.sub(/groupCode/,code)
		end
		if retstr.strip.match(/riderId/) != nil
				id = get_rider_id(json)
				retstr = retstr.sub(/riderId/,id.to_s)
		end
		return retstr
	end#make_url
	
	def get_group_code(json)
		if json["groupCode"].strip.match(/random/) == nil then return json["groupCode"] end
		min = json["groupCodeMin"]
		max = json["groupCodeMax"]
		return (json["groupCodeBase"] + @prng.rand(min...max).to_s)
	end
	
	def get_rider_id(json)
		if json["riderId"].to_s.strip.match(/random/) == nil then return json["riderId"] end
		min = json["riderIdMin"]
		max = json["riderIdMax"]
		return @prng.rand(min...max)
	end
	
end#class
