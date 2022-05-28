# Asus ROG Phone 5 Update Checker

A software update checker for the Asus ROG Phone 5. Ran daily using Github actions.

Firstly, I reverse engineered the HTTP requests waterfall on Asus' website, so that I know which one fetches the software versions.  
I then created a __Python__ script which mainly uses the `requests` library to send GET HTTP requests to that endpoint.  
(This script previously used `selenium` as well.)

This app can alternatively be run in a Docker container.

### Why did I even make this?
My device's OTA updates don't work, so I needed to notify myself somehow.  
That's how I manually update my phone, but the automatic reminder is done this way.