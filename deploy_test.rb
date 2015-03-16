#!/usr/bin/env ruby

require "date"
require 'sinatra'

enable :sessions

get '/' do
  <<-html
  <h1>Welcome</h1>
  <p>Right now it is #{DateTime.now.to_s}.</p>
  <p>Play with setting values in a <a href="/session/">Session</a></p>
html
end

def get_deploy_keys
  session
    .keys
    .keep_if { |k| k.start_with? "deploy." }
end

get '/session/' do
  if !params[:key].nil? and !params[:key].empty? then
    session["deploy.#{params[:key]}"] = params[:value]
  end

  cookie_keys = get_deploy_keys

  if cookie_keys.size == 0 then
    cookie_out = "<p>The cookie jar is empty. :( </p>"
  else
    cookie_out = "<h2>Current Cookies</h2>\n<ul>"
    cookie_keys.each do |k|
      v = session[k]
      k = k[7..-1]
      cookie_out << "<li><b>#{k}</b>: '#{v}'</li>"
    end
    cookie_out << "</ul>"
  end

  <<-html
  <h1>Sessions</h1>
  #{cookie_out}
  <form method="PUT" action="/session/">
    <label for="key">Key</label>
    <input type="input" name="key" />

    <label for="value">Value</label>
    <input type="input" name="value" />

    <input type="submit" />
  </form>
  <p><a href="/clear/">EAT ALL THE COOKIES!</a></p>
  <p>Return to <a href="/">Home</a>.</p>
html
end

get "/clear/" do
  get_deploy_keys.each do |k|
    session.delete k
  end
  redirect to('/session/')
end

