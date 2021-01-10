
import geocoding as geocode
from keys import GOOGLE_KEY, TOMTOM_KEY, HERE_KEY

#print (geocode.__version__)
#print (geocode.__doc__)


try:
	geo = geocode.Geocode()
	#result = geo.google(address='rua da boavista, nº 50', city='porto', country="Portugal", key_google=GOOGLE_KEY)
	#result = geo.tomtom(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=TOMTOM_KEY)
	result = geo.here(address='rua da boavista, nº 50', city='porto', country="Portugal", key_tomtom=HERE_KEY)

	print (result)
except Exception as e:	
	print (e)	
