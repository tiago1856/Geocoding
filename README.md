
Version: 1.0.0

# Description
* ~~Given a list of geocoding services (with the respective keys), an address and/or entity name [, city, country], it returns a json containing the geocoding results, with **'status': 'OK'**. In caso, the geocode was impossible by using every available service, then returns a json with **'status': 'UNABLE'**, with all the others fields set to None.~~
* ~~If no services are available, then an _OutOfServices_ exception will be throwed~~
* ~~In case of incorrect usage (e.g.: incorrect arguments) or some other catastrophic event, a general _Exception_ will be throwed~~


# Requirements
* Python 3.7.x
* geopy
* certifi

# Fields
* **formatted_address**
* **latitude**
* **longitude**
* **accuracy**
* **place_id**
* **type**
* **postcode**
* **input_string**
* **number_of_results**
* **status**
* **response**
* **localidade**
* **distrito**
* **concelho**
* **freguesia**
* **service**

# Available services
* Google
* TomTom
* Bing
* Here
* Nominatum
* ~~Azure~~


# Example

```python

import geocoding as geocode
from keys import GOOGLE_KEY, TOMTOM_KEY, HERE_KEY, BING_KEY

try:
	geo = geocode.Geocode()
	result1 = geo.google(address='rua da boavista, nº 50', city='porto', country="Portugal", key_google=GOOGLE_KEY)
	result2 = geo.tomtom(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=TOMTOM_KEY)
	result3 = geo.here(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=HERE_KEY)
	result4 = geo.bing(address='rua da boavista, nº 50', city='porto', country="Portugal", key_bing=BING_KEY)
	result5 = geo.nominatum(address='rua da boavista, nº 50', city='porto', country="Portugal")	
except Exception as e:	
	print (e)		
```
