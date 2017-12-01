import requests
import json
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from googleplaces import GooglePlaces, types, lang
API_KEY = 'AIzaSyC-untCAlzyRtrAuJ6ShicN0aHCHMD94jg'

google_places = GooglePlaces(API_KEY)

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html', title='Gym Finder')


@app.route('/find', methods=["GET", "POST"])
def find_gyms():
    if request.method == 'POST':
        location = request.form["location"]
        geo_coding_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ location + '&key=' + API_KEY
        geo_coding_response = json.loads(requests.get(geo_coding_url).content)
        location_coordinates = geo_coding_response["results"][0]["geometry"]["location"]
        lng = str(location_coordinates["lng"])
        lat = str(location_coordinates["lat"])
        places_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat + ',' + lng + '&rankby=distance&type=gym&key=AIzaSyC-untCAlzyRtrAuJ6ShicN0aHCHMD94jg'
        places_response = json.loads(requests.get(places_search_url).content)
        print places_search_url
        return render_template('gyms.html', gyms=places_response)
        
        
        # return "Searching for gyms around " + query_result

if __name__ == "__main__":
    app.run(debug=True)
