# Geocoding

## Version

1.0.1

##  Description
* Given an address and/or economic entity [, city, country], it returns a json containing the as much information as possible about that location/entity.
* Most services require a key to operate.

## Requirements

* Python > 3.7.x
* geopy
* certifi

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary packages.

```bash
pip install geopy
pip install certifi
```

Or just:

```bash
pip install -r requirements.txt
```


##  Returned Data
* **formatted_address**
* **latitude**
* **longitude**
* **accuracy**
* **place_id**
* **type**
* **postcode**
* **input_string**
* **number_of_results**
* **status** (OK, ZERO_RESULTS, ACCESS_ERROR, QUOTA_EXCEEDED, TIME_OUT, SERVICE_ERROR, UNKNOWN_ERROR)
* **response**
* **localidade**
* **distrito**
* **concelho**
* **freguesia**
* **service**

##  Available services
* [Google](https://cloud.google.com/maps-platform/)
* [TomTom](https://developer.tomtom.com/)
* [Here](https://developer.here.com/)
* [Bing](https://www.bingmapsportal.com/)
* [Nominatum](https://nominatim.org/)
* ~~Azure~~



## Main Functions


```python
google(self, address=None, name=None, city=None, country=None, key_google=None)
tomtom(self, address = None, city=None, country=None, key_tomtom=None)
here(self, address = None, city=None, country=None, key_tomtom=None)
bing(self, address = None, city=None, country=None, key_bing=None)
nominatum(self, address = None, city=None, country=None)
```



## Usage

```python

import geocoding as geocode
from keys import GOOGLE_KEY, TOMTOM_KEY, HERE_KEY, BING_KEY

try:
	geo = geocode.Geocode()
	result1 = geo.google(address='rua da x, nº 50', city='porto', country="Portugal", key_google=GOOGLE_KEY)
	result2 = geo.tomtom(address='rua da x, nº 50', city='porto', country="Portugal", key_tomtom=TOMTOM_KEY)
	result3 = geo.here(address='rua da x, nº 50', city='porto', country="Portugal", key_tomtom=HERE_KEY)
	result4 = geo.bing(address='rua da x, nº 50', city='porto', country="Portugal", key_bing=BING_KEY)
	result5 = geo.nominatum(address='rua da x, nº 50', city='porto', country="Portugal")	
except Exception as e:	
	print (e)		
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
