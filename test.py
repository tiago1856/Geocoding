
import geocoding as geocode

print (geocode.__version__)
print (geocode.__doc__)

GOOGLE_KEY = 'xyz'
HERE_KEY='xyz'
HERE_APP = 'xyz'
BING_KEY='xyz'
TOMTOM_KEY='xyz'

try:
	geo = geocode.Geocode()
	print(geo.google(address='rua do x, 123, Porto', country="Portugal", key_google=GOOGLE_KEY))
	print(geo.tomtom(address='rua do x, 123, Porto', country="Portugal", key_tomtom=TOMTOM_KEY))
	print(geo.here(address='rua do x, 123, Porto', country="Portugal", key_tomtom=HERE_KEY))
	print(geo.bing(address='rua do x, 123, Porto', country="Portugal", key_bing=BING_KEY))
	print(geo.nominatum(address='rua do x, 123, Porto', country="Portugal"))
except Exception as e:	
	print (e)	
