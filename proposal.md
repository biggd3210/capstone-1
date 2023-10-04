

Capstone 1 Proposal
===================

1. What goal will your website be designed to achieve?

    > Allow people to store trip itinerary and share among friends or family. Possibly allow for voting. 

2. what kind of users will visit/what demographic are we aiming for?
   
    > Families or individual travelers.

3. What data do you plan on using? What kind of API do you want to use?

    > Travel API's. Flight planner. maybe accomodations. Perhaps more than one if necessary.
    > User tables will start out small. Mainly username, password, email, f-name, l-name, phone.
    >> email and phone will be utilized to send links to other users or 3rd party people.
    > A user should be able to search for any piece of a trip and save that piece individually. Then, a user should be able to link pieces of a trip together into one record of itinerary. Can also link multiple users into one itinerary if the travel group is more than one person. 

4. In brief, outline your approach to creating your project.
   1. What does your DB schema look like?
        > table for itinerary. can hold multiple pieces from users table, flights table, or accommodations table.
   2. what kinds of issues might you run into with the API?
        > not yet sure. Have to do more research into available API's to see what is available and what features would be most useful. 
   3. Is there sensitive information you need to secure?
        > Perhaps. I don't plan on containing any sensitive information. But coudl potentially (far down the line, contain known traveler number to prepopulate a booking page. But I doubt it.)
   4. What functionality will your app include?
        > Flask, WTforms, Interactive Map to show routes. JS. 
   5. What will user flow look like?
        > Landing page will show a map with anonymous travel routes. Once registered or logged in, user will land on map of currently planned trips in which the user is included. nav bar will allow for options to query itineraries or quick search for flights or accommodations or excursions. Can save searches and link searches together in itinerary records. 
   6. What features make your site more than CRUD? Stretch goals?
        > email feature to share link with family or friends. Can link users together so multiple people can see the same info. Useful in allowing large groups to plan a trip that suits the needs for as many travelers as possible. 