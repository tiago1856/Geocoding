#import pandas as pd
#import logging
#import time
import re
#import random
import csv



from geopy.geocoders import GoogleV3
from geopy.geocoders import TomTom
from geopy.geocoders import Bing
from geopy.geocoders import Here
from geopy.geocoders import Nominatim
#from geopy.geocoders import AzureMaps

from geopy.exc import (
    GeocoderQueryError,
    GeocoderQuotaExceeded,
    ConfigurationError,
    GeocoderParseError,
    GeocoderAuthenticationFailure,
    GeocoderInsufficientPrivileges,
    GeocoderTimedOut,
    GeocoderServiceError,
    GeocoderUnavailable,
    GeocoderNotFound
)


import ssl
import certifi
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx



############ logging ############

#logger = logging.getLogger("root")
#logger.setLevel(logging.DEBUG)
#create console handler
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)


############ ERRORS ############

class UnableToGeocode(Exception): 
	# Constructor or Initializer 
	def __init__(self, value): 
		self.value = value 
  
	# __str__ is to print() the value 
	def __str__(self): 
		return(repr(self.value)) 
		
class Geocode():

	def __init__(self):
		pass


	############ SERVICES ############

	def newResult(self):
		output={}
		output["formatted_address"] = None
		output["latitude"] = None
		output["longitude"] = None
		output["accuracy"] = None
		output["place_id"] = None
		output["type"] = None
		output["postcode"] = None
		output["input_string"] = None
		output["number_of_results"] = None
		output["status"] = None
		output["response"] = None
		output["city"] = None
		output["distrito"] = None
		output["concelho"] = None
		output["freguesia"] = None	
		output["service"] = None
		return output
		
		

	def google(self, address=None, name=None, city=None, country=None, key_google=None):
		if not key_google:
			raise RuntimeError("Requires a key! Check https://cloud.google.com/maps-platform/ for more information.")
		if not address and not name and not city and not country:
			raise RuntimeError("Requires name and/or an address and/or a city and/or a country!")

		addr = "" if name is None else name
		addr += ("" if address is None else ", " + address)
		addr += ("" if city is None else ", " + city)
		addr += ("" if country is None else ", " + country)

		result = self.newResult()
		result['service']  = 'google'
		result['status'] = 'ZERO_RESULTS'

		try:
			# start service
			geolocator_google = GoogleV3(api_key=key_google)
			# fetch the data
			data = geolocator_google.geocode(addr,exactly_one=False)
			if data:			
				answer = data[0].raw
				result['status'] = "OK"		
				result["formatted_address"] = data[0].address
				result["latitude"] = data[0].latitude
				result["longitude"] = data[0].longitude
				result["accuracy"] = answer.get('geometry').get('location_type')
				result["place_id"] = answer.get("place_id")
				result["type"] = ",".join(answer.get('types'))
				result["postcode"] = ",".join([x['long_name'] for x in answer.get('address_components') 
									  if 'postal_code' in x.get('types')])
				result["input_string"] = address
				result["number_of_results"] = len(data)
				result["localidade"] = ",".join([x['long_name'] for x in answer.get('address_components') 
									  if 'locality' in x.get('types')]).split(',')[0]


		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception as e:
			result['status'] = 'UNKNOWN_ERROR'

		
		return result




	def tomtom(self, address = None, city=None, country=None, key_tomtom=None):

		if not key_tomtom:
			raise RuntimeError("Requires a key! Check https://developer.tomtom.com/ for more information.")
		if not address and not city and not country:
			raise RuntimeError("Requires an address and/or a city and/or a country!")

		addr = "" if address is None else address
		#addr = ("" if address is None else ", " + address)
		addr += ("" if city is None else ", " + city)
		addr += ("" if country is None else ", " + country)

		result = self.newResult()
		result['service']  = 'tomtom'
		result['status'] = 'ZERO_RESULTS'


		try:	
			geolocator_tomtom = TomTom(api_key=key_tomtom)
			location = geolocator_tomtom.geocode(addr, exactly_one=False)
			if location is not None:
				answer = location[0].raw
				
				result['status'] = "OK"
				result["latitude"] = location[0].latitude
				result["longitude"] = location[0].longitude
				
				result["accuracy"] = answer.get('score')
				result["input_string"] = address
				result["number_of_results"] = len(location)#answer.get("numResults")
				result["place_id"] = answer.get("id")
				
				if answer.get("address"):
					result["distrito"] = answer.get("address").get("countrySubdivision")
					# maybe?
					result["concelho"] = answer.get("address").get("municipality")
					result["freguesia"] = answer.get("address").get("municipalitySubdivision")
					result["formatted_address"] = answer.get('address').get('freeformAddress')
					CPext = answer.get("address").get('extendedPostalCode')
					CP = answer.get("address").get('postalCode')
					if CPext:
						CPext = CPext.split(',')[0]
						CPext = CPext[:4] + '-' + CPext[4:]
						result["postcode"] = CPext
					elif CP:
						result["postcode"] = CP.split(',')[0]
					
					
					
				result["type"] = answer.get('type')
				#result["query_type"] = answer.get("queryType")
				
				# maybe?
				#result["localidade"] = answer.get("address").get("municipality")	
				
				#if saveraw:
				#	result["response"] = location[0].raw
				# 	

		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception as e:
			result['status'] = 'UNKNOWN_ERROR'
		
		return result


	def here(self, address = None, city=None, country=None, key_here=None):

		if not key_here:
			raise RuntimeError("Requires a key! Check https://developer.here.com/ for more information.")
		if not address and not city and not country:
			raise RuntimeError("Requires an address and/or a city and/or a country!")


		addr = "" if address is None else address
		#addr = ("" if address is None else ", " + address)
		addr += ("" if city is None else ", " + city)
		addr += ("" if country is None else ", " + country)

		result = self.newResult()
		result['service']  = 'here'
		result['status'] = 'ZERO_RESULTS'


		try:		
			geolocator_here = Here(apikey=key_here)
			location = geolocator_here.geocode(addr, exactly_one=False,language="pt-PT")

			if location is not None:
				answer = location[0].raw
				
				result['status'] = "OK"
				result["latitude"] = location[0].latitude
				result["longitude"] = location[0].longitude
				result["number_of_results"] = len(location)
				
				result["input_string"] = address
				
				result["accuracy"] = answer.get('Relevance')
				
				if answer.get("Location"):
					result["formatted_address"] = answer.get("Location").get('Address').get('Label')
					result["place_id"] = answer.get("Location").get("LocationId")
					
				
				if answer.get("Location"):
					if answer.get("Location").get("Address"):
						result["postcode"] = answer.get("Location").get("Address").get("PostalCode")	
						# all 4 are not tghrustworthy
						result["freguesia"] = answer.get("Location").get("Address").get("District")		
						result["distrito"] = answer.get("Location").get("Address").get("County")
						result["concelho"] = answer.get("Location").get("Address").get("City")
						result["localidade"] = answer.get("Location").get("Address").get("City")		
				
				#if saveraw:
				#	output["response"] = location[0].raw

		
		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception as e:
			result['status'] = 'UNKNOWN_ERROR'
		
		return result




	def bing(self, address = None, city=None, country=None, key_bing=None):

		if not key_bing:
			raise RuntimeError("Requires a key! Check https://www.bingmapsportal.com/ for more information.")
		if not address and not city and not country:
			raise RuntimeError("Requires an address and/or a city and/or a country!")

		addr = "" if address is None else address
		#addr = ("" if address is None else ", " + address)
		addr += ("" if city is None else ", " + city)
		addr += ("" if country is None else ", " + country)

		result = self.newResult()
		result['service']  = 'bing'
		result['status'] = 'ZERO_RESULTS'


		try:		
			geolocator_bing = Bing(api_key=key_bing)
			location = geolocator_bing.geocode(address,  exactly_one=False) #culture='PT',  include_neighborhood=True,
			if location is not None:
				answer = location[0].raw
				
				result['status'] = "OK"
				result["latitude"] = location[0].latitude
				result["longitude"] = location[0].longitude
				result["number_of_results"] = len(location)
				
				
				if answer.get("address"):
					result["formatted_address"] = answer.get('address').get('formattedAddress')
					result["localidade"] = answer.get("address").get("locality")
					result["distrito"] = answer.get("address").get("adminDistrict")
					result["concelho"] = answer.get("address").get("adminDistrict2")
					result["freguesia"] = answer.get("address").get("neighborhood")		
					result["postcode"] = answer.get("address").get("postalCode")
				
				result["accuracy"] = answer.get('confidence')
				
				result["input_string"] = address								

			#	if saveraw:
			#		result["response"] = location[0].raw	
		
		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception as e:
			result['status'] = 'UNKNOWN_ERROR'
		
		return result


	def nominatum(self, address = None, city=None, country=None):

		if not address and not city and not country:
			raise RuntimeError("Requires an address and/or a city and/or a country!")

		addr = "" if address is None else address
		#addr = ("" if address is None else ", " + address)
		addr += ("" if city is None else ", " + city)
		addr += ("" if country is None else ", " + country)

		result = self.newResult()
		result['service']  = 'nominatum'
		result['status'] = 'ZERO_RESULTS'


		try:		
			geolocator_nominatum = Nominatim(user_agent="tests_1")			
			location = geolocator_nominatum.geocode(address, exactly_one=False,  addressdetails=True)
			if location is not None:
				answer = location[0].raw
				
				result['status'] = "OK"
				result["latitude"] = location[0].latitude
				result["longitude"] = location[0].longitude
				result["number_of_results"] = len(location)
				#result["accuracy"] = answer.get('importance')
				result["place_id"] = answer.get("osm_id")
				result["input_string"] = address
				if answer.get("address"):
					result["postcode"] = re.sub('[^0-9-]+', '', answer.get("address").get("postcode")) ###???
					result["freguesia"] = answer.get("address").get("suburb")
					result["localidade"] = answer.get("address").get("city")
					if not result["localidade"]:
						result["localidade"] = answer.get("address").get("town")
					result["formatted_address"] = answer.get('address').get('display_name')
					
				result["type"] = answer.get('osm_type')
				
				
				#if saveraw:
				#	result["response"] = location[0].raw		

		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception as e:
			print(e)
			result['status'] = 'UNKNOWN_ERROR'
		
		return result



	###
	'''
	def azure(self, addr, local, country, saveraw):
		output=self.initOutput()	
		
		# create query	
		address = "" if addr is None else addr
		address = address + ("" if local is None else "," + local)
		address = address + ("" if country is None else "," + country)
		
		
		# init service if not init yet
		if not self.geolocator_azure:		
			self.geolocator_azure = AzureMaps(subscription_key=self.SERVICES[self.CURRENT_SERVICE]['key'])


		# geocode address
		location = self.geolocator_azure.geocode(address, exactly_one=False,language="pt-PT")
		if location is not None:
			answer = location[0].raw
			
			output['status'] = "OK"
			output["latitude"] = location[0].latitude
			output["longitude"] = location[0].longitude
			output["number_of_results"] = len(location)
			
			output["input_string"] = address
			
			output["accuracy"] = answer.get('score')
			
			output["place_id"] = answer.get("id")
			
			if answer.get("address"):
				output["formatted_address"] = answer.get('address').get('freeformAddress')
				output["distrito"] = answer.get("address").get("countrySubdivision")
				# maybe?
				output["concelho"] = answer.get("address").get("municipality")
				output["freguesia"] = answer.get("address").get("municipalitySubdivision")
				CPext = answer.get("address").get('extendedPostalCode')
				CP = answer.get("address").get('postalCode')
				if CPext:
					CPext = CPext.split(',')[0]
					CPext = CPext[:4] + '-' + CPext[4:]
					output["postcode"] = CPext
				elif CP:
					output["postcode"] = CP.split(',')[0]
			
			output["type"] = answer.get('type')			

			output["service"] = self.SERVICES[self.CURRENT_SERVICE]['service']			

			if saveraw:				
				output["response"] = location[0].raw		

		else:
			output['status'] = "ZERO_RESULTS"
		
		return output
	'''

		
