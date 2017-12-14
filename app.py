import requests
import pyrebase
from hashids import Hashids
from flask import Flask, render_template, url_for, request, redirect

hashid_salt = 'impossible to guess'
hashids = Hashids(salt=hashid_salt, min_length=4)


API_KEY = 'AIzaSyC-untCAlzyRtrAuJ6ShicN0aHCHMD94jg'

firebase_config = {
  "apiKey": "AIzaSyAJGhs8jr8RTdUYtKGDx0dwAZ_03MySDH0",
  "authDomain": "gym-finder-1512123683114.firebaseapp.com",
  "databaseURL": "https://gym-finder-1512123683114.firebaseio.com",
  "storageBucket": "gym-finder-1512123683114.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Nothing Here for now'

@app.route('/gym')
def gym_page():
    return render_template('index.html')

@app.route('/gym/find', methods=["POST"])
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
        new_booking_id = None
        try:
            bookings = db.child("bookings").get().val()
            booking_id = [entry for entry in bookings][-1]['id']
            new_booking_id = int(booking_id) + 1
        except:
            new_booking_id = 0
        
        new_booking_ref = db.child("bookings").child(new_booking_id)
        booking_id_string = hashids.encode(new_booking_id)
        booking_confirm_url = 'session/confirm/' + booking_id_string
        booking_details = dict()
        booking_details['id'] = int(new_booking_id)
        booking_details['name'] = request.form["name"]
        booking_details['phone_number'] = request.form["phone"]
        booking_details['email'] = request.form['email']
        booking_details['date_time'] = request.form['date_time']
        booking_details['id_string'] = booking_id_string
        new_booking_ref.set(booking_details)
        return redirect(booking_confirm_url)


@app.route('/session/confirm/<booking_id>')       
def display_confirmation(booking_id):
    real_booking_id = hashids.decode(booking_id)[0]
    booking_ref = db.child('bookings').child(real_booking_id)
    result = booking_ref.get().val()
    booking_details = dict(result)
    return render_template('confirm.html', booking_details=booking_details)


if __name__ == "__main__":
    app.run()
