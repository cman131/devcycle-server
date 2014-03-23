#!/usr/bin/ruby

require 'faraday' #http client lib

require 'typhoeus' #parallel http requests WAITING FOR V 0.6.7 for patch current 0.6.6 is buggy this won't work

require 'typhoeus/adapters/faraday' #typhoeus adapter

require 'benchmark' #measurements/stats

require 'json'

require_relative 'response_handler'


@configs
@url
@manager

class Load_Test

    def initialize(configs)
      @configs = configs
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

      conn.post do |request|

        request.url @url

        request.headers['Content-Type'] = 'application/json'

        request.body = json.to_json

      end#conn.post


    end#post


end#class
