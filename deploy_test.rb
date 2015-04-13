#!/usr/bin/env ruby

require "date"
require 'sinatra'

class Application < Sinatra::Base
  get '/' do
    erb :index
  end
end
