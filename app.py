import requests
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect , jsonify

API_KEY = 'AIzaSyC-untCAlzyRtrAuJ6ShicN0aHCHMD94jg'

app = Flask(__name__)


@app.route('/')
def home_page():
    return 'Nothing Here for now'

@app.route('/gym')
def gym_page():
    return render_template('index.html', title='Gym Finder')


@app.route('/gym/find', methods=["GET", "POST"])
def find_gyms():
    if request.method == 'POST':
        location = request.form["location"]
        geo_coding_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ location + '&key=' + API_KEY
        geo_coding_response = requests.get(geo_coding_url).json()
        location_coordinates = geo_coding_response["results"][0]["geometry"]["location"]
        lng = str(location_coordinates["lng"])
        lat = str(location_coordinates["lat"])
        places_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat + ',' + lng + '&rankby=distance&type=gym&keyword=gym&key=AIzaSyC-untCAlzyRtrAuJ6ShicN0aHCHMD94jg'
        places_response = requests.get(places_search_url).json()
        return render_template('gyms.html', gyms=places_response)

@app.route('/gym/more/<place_id>', methods=["GET", "POST"])
def gym_info(place_id):
    if request.method == 'GET':
        place_api_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=AIzaSyDHHLWzJzlZZFDye9JbxiCu4RXei_bzMbE'
        place_details_response = requests.get(place_api_url).json()
        return render_template('gym.html', gym=place_details_response)
    if request.method == 'POST':
        booking_details = dict()
        booking_details['name'] = request.form["name"]
        booking_details['phone_number'] = request.form["phone"]
        booking_details['email'] = request.form['email']
        booking_details['date_time'] = request.form['date_time']
        place_api_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=AIzaSyDHHLWzJzlZZFDye9JbxiCu4RXei_bzMbE'
        place_details_response = requests.get(place_api_url).json()
        return render_template('confirm.html', booking_details=booking_details)

if __name__ == "__main__":
    app.run(debug = True)
