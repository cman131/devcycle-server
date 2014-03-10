#!/usr/bin/ruby

require 'typhoeus'
require 'benchmark'
require 'json'

hydra = Typhoeus::Hydra.hydra

Typhoeus::Hydra.new(max_concurrency: 200)
done = 0

example_params = JSON.parse(IO.read('example.json'))

Benchmark.bm(25) do |x|
  x.report do
    for i in 1..32000
      req = Typhoeus::Request.new("http://devcycle.se.rit.edu/location_update", params: example_params)

      req.on_complete do |response|
        done = done+1
        puts "Done! #{done}"
      end
      hydra.queue req
    end

    puts "Here we gooooooooo...."
    hydra.run
  end
end

