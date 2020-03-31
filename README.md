# BoozeCruiseYYC

![](https://img.shields.io/github/license/AntonBiryukovUofC/boozecruiseyyc?style=for-the-badge) ![](https://img.shields.io/github/v/release/AntonBiryukovUofC/boozecruiseyyc?style=for-the-badge) ![](https://img.shields.io/circleci/build/github/AntonBiryukovUofC/boozecruiseyyc/master?style=for-the-badge)

Delivery routing with the original purpose to figure out the best route to drop off beer at many locations around YYC.

## Functionality / Components

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

