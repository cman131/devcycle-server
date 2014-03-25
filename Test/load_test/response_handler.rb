require 'typhoeus/adapters/faraday'

require 'benchmark'

# Handles the response returned by the Post 
# Request to the Server. Prints it out
#
class LoadTestHandler < Faraday::Response::Middleware
	@@response_count = 0

	def call(env)
		@@response_count+=1
		 # "env" contains the request
	    @app.call(env).on_complete do
	      # "env" contains the request AND response
	      response = {
	        request_url: env[:url].to_s,
	        response_status: env[:response].status,
	        response_body: env[:response].body
	      }

	      p "Response #{@@response_count}: #{response}"

	    end#on_complete

	end#call

end#class