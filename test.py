
import geocoding as geocode
from keys import GOOGLE_KEY

#print (geocode.__version__)
#print (geocode.__doc__)


try:
	geo = geocode.Geocode()
	result = geo.google(address='rua da boavista, nº 50', city='porto', country="Portugal", key_google=GOOGLE_KEY)
	print (result)
except Exception as e:	
	print (e)	
