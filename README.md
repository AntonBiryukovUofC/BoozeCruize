# BoozeCruizeYYC

### Preamble

Before COVID-19 we used to have occasional beer tastings with my co-workers, which we used as a way to un-wind after a
productive week, as well as support local breweries. The preparatory ritual involved buying a few local craft tallboys
at a nearby liquor store.

After COVID-19 forced Calgary into a full lock-down, we continued with our tradition, with a slight twist. One of us would
have to volunteer themselves and deliver beer to their colleagues. Unfortunately, this came with the time cost as whole ETB
Calgary crew is well-spread around the city. As a result, it is not that trivial to figure out how to navigate your way aorund town
and visit every member in the most time-efficient manner. Therefore, I decided to simplify the process and started developing this app
together with @mikebirdgeneau and @Brayden-Arthur.

**BoozeCruizeYYC**:
Delivery routing with the original purpose to figure out the best route to drop off beer at many locations around YYC.

### What it does

Given a set of destinations points (places you have to visit), as well as starting and ending point of your journey,
the app provides you with the time-efficient route order, as well as a navigation link for Google Maps. This allows you
to have familiar navigation workflow - just like you'd follow when getting to a new Thai restaurant  in a neighbourhood
 you never been before!



![](https://img.shields.io/github/license/AntonBiryukovUofC/boozecruiseyyc?style=for-the-badge)
![](https://img.shields.io/github/v/release/AntonBiryukovUofC/boozecruiseyyc?style=for-the-badge)
![](https://img.shields.io/circleci/build/github/AntonBiryukovUofC/boozecruiseyyc/master?style=for-the-badge)

### How to use

Here is a typical step-by-step guide on using the web app (assuming you have it running in your browser tab):

1. Fill out the Departure Point. Tick the box if Final Destination is different from Departure Point, and fill that one too.
2. Using top slider, pick the number of locations you need to visit
3. Fill each Destination point field, in no order
    - you can do that either manually, or
    - in batch manner by copy-pasting from Excel Spreadsheet like shown before
4. Click Optimize Route button, and wait till we do our routing magic!
5. Watch the optimal route appear on the map, and make sure it looks correct (sometimes geocoding can miss a location!)
6. Your URL for Google Maps will be posted under the graph showing the route - clicking it on either mobile or desktop
will pop up Google Maps with navigation mode on. All you need is to click Navigate, and off you go!

### Docker

To launch this app using docker, please make sure you have the [Docker Engine](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed. (Note that on Mac / Windows desktop installs, compose is included; however, on Linux it ust be installed separately.)

With your working directory set to the root of this repository (same directory as the `docker-compose.yml` file), run:

```
export API_KEY_TOMTOM='<<YOUR API KEY FOR TOMTOM>>'
export API_KEY_HERE='<<YOUR API KEY FOR HERE>>'
docker-compose build && docker-compose up -d
```

Docker will pull all the required images and start the application at the following URL: [http://localhost:5006/app](http://localhost:5006/app).


## Functionality / Components (a.k.a. How it works)





- Click on a Map, get a validated address; Type an Address, get a validated address 
  - Nominatim: Free & hosted, but has some issues with address validation (at least in Calgary).
  - Mapquest: 2500 monthly requests; autocomplete might exceed...
  - Google: $0.005 USD per request.
  - Tomtom: 2500 requests daily. Seems good!
- Provide a start point, list of addresses, and end-point, get a optimal routing.
  - Same API options as above.
- Export results to google maps
  - https://developers.google.com/maps/documentation/urls/guide#directions-action
- UI
  - Holoviz Panel?

- CI / Deployment
  - Docker

