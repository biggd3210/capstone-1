# Mappo-Pollo

### What can you do?
Mappo-Pollo is a simple webapp that allows the user to search for flights and accomodations and organize them into an itinerary collection. The user has the option to share a link to that itinerary with a friend via email. 

### Where can you find it?
Mappo-Pollo is deployed on Render, found [here](https://mappo-pollo.onrender.com). If the link doesn't work you can copy this url:  
```https://mappo-pollo.onrender.com```

### Flow:
A user will create an account and then have access to search for flights or accommodations. For flights, there is one form and one results page. For accommodations, due to Amadeus's API, the simplest method was to search for rooms to first find hotels in the given area. This populates a list of hotels. Each hotel card has a button that allows the user to search a particular hotel for an available room. Once a hotel or room has been selected, it can be added to an itinerary. Either a previously existing itinerary or the user can make a new one.  
From the nav bar, a user can view the itineraries they've made. From an itinerary view page, the user can view the full itinerary including all the itinerary components. From an itinerary view page, the user can delete any components, the full itinerary, or share the itinerary. 
To share, a modal will populate with from, to, subject, and message. It will include a link to view the itinerary. When a user clicks share, it will ping MailJet to automatically send an email to the provided email address. 

### Caveats:
- In order to use search functionality correctly, user must input 3 character IATA code.  
Orlando -> MCO, New York City -> NYC, London -> LHR.  
- The API server is temporary testing server and therefore does not have access to all locations. Therefore, some smaller airports or cities may not produce any viable results for a search. 

### Goals and Future plans:
Include an auto-complete feature for city search functions.  
Modify calendar inputs to improve user functionality.  
Allow for search functionality including excursions, activities, etc. 

### Technology Stack:
OS and programming languages: Python and JS  
Backend Framework: Flask/SQL-Alchemy  
Frontend Frameworks: Bootstrap, jQuery  
Database: PostgresSQL

API: [ Base URL: test.api.amadeus.com/v2 ]

