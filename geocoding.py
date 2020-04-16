import requests
import json

filePath = "Covid-19.csv" #original
filePathWithGeo = "Covid-19-geo.csv" #with geo data
filePathGeocodesOnly = "geocodes.txt" #Geocodes

geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDRVlOny0TLwFDTYkHhKBKMdW8iJXLLpmg&address="

counter = 0;

with open(filePath, "r") as f:
	next(f) 
	for line in f:
		print("Comment break function due to expensive call")
		break

		counter = counter + 1
		if counter < 62:
			continue

		lineArr = [x.strip() for x in line.split(',')] # convert line string to array
		address = lineArr[0]+' '+lineArr[1]+' '+lineArr[2]+' '+lineArr[3] # extract address info

		r = requests.get(geocodeUrl+address) # get geocoding data by address
		data = json.loads(r.content) # convert string to json

		if len(data["results"]) == 0:
			print(address+" (ZERO_RESULTS)")
			continue
		else:
			print(address)

		#{'results': [{'address_components': [{'long_name': 'Arica', 'short_name': 'Arica', 'types': ['locality', 'political']}, {'long_name': 'Arica', 'short_name': 'Arica', 'types': ['administrative_area_level_3', 'political']}, {'long_name': 'Arica Province', 'short_name': 'Arica Province', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Arica y Parinacota', 'short_name': 'Arica y Parinacota', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Chile', 'short_name': 'CL', 'types': ['country', 'political']}], 'formatted_address': 'Arica, Arica y Parinacota, Chile', 'geometry': {'bounds': {'northeast': {'lat': -18.4228594, 'lng': -70.2445165}, 'southwest': {'lat': -18.522094, 'lng': -70.33377879999999}}, 'location': {'lat': -18.4782534, 'lng': -70.3125988}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': -18.4228594, 'lng': -70.2445165}, 'southwest': {'lat': -18.522094, 'lng': -70.33377879999999}}}, 'partial_match': True, 'place_id': 'ChIJNcIy2YqpWpERHdfYBGyI9Sc', 'types': ['locality', 'political']}], 'status': 'OK'}
		lat = data["results"][0]["geometry"]["location"]["lat"]
		lng = data["results"][0]["geometry"]["location"]["lng"]

		with open(filePathWithGeo, "a") as myfile:
			myfile.write(str(lat)+","+str(lng)+","+line)

		with open(filePathGeocodesOnly, 'a') as the_file:
			the_file.write(str(data)+"\n")