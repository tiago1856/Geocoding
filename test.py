
import geocoding as geocode
from keys import GOOGLE_KEY, TOMTOM_KEY, HERE_KEY, BING_KEY

print (geocode.__version__)
print (geocode.__doc__)


try:
	geo = geocode.Geocode()
	result1 = geo.google(address='rua da boavista, nº 50', city='porto', country="Portugal", key_google=GOOGLE_KEY)
	result2 = geo.tomtom(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=TOMTOM_KEY)
	result3 = geo.here(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=HERE_KEY)
	result4 = geo.bing(address='rua da boavista, nº 50', city='porto', country="Portugal", key_bing=BING_KEY)
	result5 = geo.nominatum(address='rua da boavista, nº 50', city='porto', country="Portugal")	
except Exception as e:	
	print (e)	
