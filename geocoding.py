from bs4 import BeautifulSoup
import requests
import json
import urllib
from datetime import date, timedelta

today = date.today().strftime("%Y-%m-%d")
yesterday = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
print(today,yesterday)

geocodingFile = "geocodes.txt" #Geocodes
geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json?key=SECRETKEY&address="
remoteCsvFile = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/"+yesterday+"-CasosConfirmados-totalRegional.csv"
localCsvFile = yesterday+"-CasosConfirmados-totalRegional.csv"
localCsvGeoFile = yesterday+"-CasosConfirmados-totalRegional-geo.csv"


urllib.request.urlretrieve(remoteCsvFile,localCsvFile)

counter = 0;
with open(localCsvFile, "r") as f:
	next(f) 
	for line in f:
		#print("Comment break function due to expensive call")
		#break

		counter = counter + 1
		lineArr = [x.strip() for x in line.split(',')] # convert line string to array
		address = lineArr[0] # extract address info

		r = requests.get(geocodeUrl+address+" Chile") # get geocoding data by address and country 
		data = json.loads(r.content) # convert string to json

		if len(data["results"]) == 0:
			print(address+" (ZERO_RESULTS)")
			continue
		else:
			print(address)

		lat = data["results"][0]["geometry"]["location"]["lat"]
		lng = data["results"][0]["geometry"]["location"]["lng"]

		with open(localCsvGeoFile, "a") as myfile:
			myfile.write(str(lat)+","+str(lng)+","+line)

		with open(geocodingFile, 'a') as the_file:
			the_file.write(str(data)+"\n")