"""Communications for Amadeus API's."""

from secret import AMADEUS_API_KEY, AMADEUS_API_SECRET, MAILJET_API_KEY, MAILJET_SECRET_KEY
import requests, json
from amadeus import Client, ResponseError
from helpers import format_date, format_time, format_date_time

amadeus = Client(
    client_id = AMADEUS_API_KEY,
    client_secret = AMADEUS_API_SECRET
)

from mailjet_rest import Client

mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3')

# -------------- *****------------------
# Amadeus API information. Note some routes require v1 and some require v2. 'v1 / v2' left off base url and affixed to route variable.

base_url = 'https://test.api.amadeus.com/'
endpoint_auth = 'v1/security/oauth2/token'
endpoint_flight_search = 'v2/shopping/flight-offers'
endpoint_cities = 'v1/reference-data/locations/cities'

def request_amadeus_auth():
    """Make a request to obtain an authorization key to use in route requests for API information. Auth Key expires and must be renewed."""

    url = f'{base_url}{endpoint_auth}'
    resp = requests.post(url,
                         headers={
                             "Content-Type": "application/x-www-form-urlencoded"
                         },
                         data = {
                             "grant_type":  "client_credentials",
                             "client_id": AMADEUS_API_KEY,
                             "client_secret": AMADEUS_API_SECRET
                         })
    if resp:
        token = resp.json()['access_token']
    return token

# ---------- Airline/Flight searches -----------

def format_flight_data(jobj):
        """takes response data from API call and harvests info to be displayed on website. """

        boomerang = []

        for flight in jobj:
            """grab info about each flight offer."""
            num_segments = len(flight['itineraries'][0]['segments'])
            carriercode = resolve_carriercode(flight.get('validatingAirlineCodes')[0])
            option = {
            "id" : flight['id'],
            "origin" : flight.get('itineraries', "Null")[0].get('segments')[0].get('departure').get('iataCode'),
            "destination" : flight.get('itineraries', "Null")[0].get('segments')[num_segments - 1].get('arrival').get('iataCode'),
            "departure date" : flight.get('itineraries', "Null")[0].get('segments')[0].get('departure').get('at'),
            "arrival date" : flight.get('itineraries', "Null")[0].get('segments')[num_segments - 1].get('arrival').get('at'),
            "duration" : flight.get('itineraries', "Null")[0].get('duration'),
            "segments" : len(flight['itineraries'][0]['segments']),
            "price" : flight.get('price', "Null").get('total'),
            "seats remaining" : flight.get("numberOfBookableSeats", "Null"),
            "travelers" : len(flight['travelerPricings']),
            "currency" : flight.get('price', "Null").get('currency'),
            "carrier" : carriercode,
            "iataCode" : flight.get('validatingAirlineCodes')[0],
            "componentType" : "flight"
            }
            
            id = flight['id']
            
            boomerang.append(option)

        return boomerang

def search_available_flights(params):
    """uses form search criteria to locate available flights."""

    try: 
        if params['returnDate']:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=params['origin'],
                destinationLocationCode=params['destination'],
                departureDate=params['departureDate'],
                returnDate=params['returnDate'],
                adults=params['px_num'],
                currencyCode="USD",
                max=30
            )
        else:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=params['origin'],
                destinationLocationCode=params['destination'],
                departureDate=params['departureDate'],
                adults=params['px_num'],
                currencyCode="USD",
                max=30
            )
        resp = format_flight_data(response.data)
             
        return resp
    
    except ResponseError as error:
        print(error)

def resolve_carriercode(carrier_code):
    """
    converts returned IATA code from search to user readible airline name.
    ex: F9 ---> Frontier Airlines
    """
    params = {
        "iataCode" : carrier_code
    }
    try:
        response = amadeus.reference_data.airlines.get(
            airlineCodes=carrier_code
        )
        return response.data[0]['commonName']

    except ResponseError as error:
        print(error)


# --------- Accommodations Searches --------

def format_hotel_data(jobj):
    """converts JSON from API to usable list for app."""

    boomerang = []

    for hotel in jobj:
        option = {
            "chainCode": hotel['chainCode'],
            "iataCode": hotel['iataCode'],
            "hotel_name": hotel['name'],
            "latitude": hotel['geoCode']['latitude'],
            "longitude": hotel['geoCode']['longitude'],
            "hotelId": hotel['hotelId'],
            "componentType" : "accom"
        }
        boomerang.append(option)
    
    return boomerang

def search_accommodations(params):
    """takes params from search form and creates request from Amadeus API."""

    resp = amadeus.reference_data.locations.hotels.by_city.get(
        cityCode=params['cityCode'],
        radius=params['radius'],
        radiusUnit=params['radiusUnit']
    )
    hotels = format_hotel_data(resp.data)
    return hotels

def format_room_data(jobj):
    """returns useable info from hotel room offers API."""

    boomerang = {}

    boomerang['hotelId'] = jobj[0]['hotel']['hotelId']
    boomerang['longitude'] = jobj[0]['hotel']['longitude']
    boomerang['latitude'] = jobj[0]['hotel']['latitude']
    boomerang['hotelName'] = jobj[0]['hotel']['name']
    boomerang['checkInDate'] = jobj[0]['offers'][0]['checkInDate']
    boomerang['checkOutDate'] = jobj[0]['offers'][0]['checkOutDate']
    boomerang['numOfGuests'] = jobj[0]['offers'][0]['guests']['adults']
    boomerang['price'] = jobj[0]['offers'][0]['price']['total']
    boomerang['currency'] = jobj[0]['offers'][0]['price']['currency']

    return boomerang


def search_hotel_offers(params):
    """Searches api for room offers of hotels."""

    resp = amadeus.shopping.hotel_offers_search.get(
        hotelIds=params['hotelIds'],
        adults=params['adults'],
        checkInDate= '2023-12-20',
        checkOutDate= '2023-12-21'
    )
    print('------------------------------')
    print('resp from search_hotel_offers() is ', resp.data)
    print('---------------------------------')
    return resp.data

def share_itinerary_mailjet(params):
    """calls to mailjet API to share link to itinerary."""

    res = mailjet.send.create(data=params)
    status = res.json()

    return status