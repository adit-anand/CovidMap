from bs4 import BeautifulSoup
import requests
import json
import urllib

filePath = "Covid-19.csv" #original
filePathWithGeo = "Covid-19-geo.csv" #with geo data
filePathGeocodesOnly = "geocodes.txt" #Geocodes
geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json?key=SECRETKEY&address="
dataSrcBaseUrls = "https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto4"

def getLatestDataSrcUrl():
	req = requests.get(dataSrcBaseUrls, requests.utils.default_headers())
	soup = BeautifulSoup(req.content, 'html.parser')
	dataFileUrls = []
	dataFileUrlLatest = ""
	for a in soup.find_all('a', href=True):
		if a['href'].endswith(".csv"):
			dataFileUrls.append(str(a['href']))
	dataFileUrlLatest = "https://raw.githubusercontent.com" + dataFileUrls[len(dataFileUrls)-1].replace("/blob","")
	print("Found the latest data file:", dataFileUrlLatest)
	return dataFileUrlLatest

def getLatestDataSrcFileByUrl():
	urllib.request.urlretrieve(getLatestDataSrcUrl(),"Covid-19.csv")


counter = 0;
with open(filePath, "r") as f:
	next(f) 
	for line in f:
		print("Comment break function due to expensive call")
		break

		counter = counter + 1
		lineArr = [x.strip() for x in line.split(',')] # convert line string to array
		address = lineArr[0] # extract address info

		r = requests.get(geocodeUrl+address) # get geocoding data by address
		data = json.loads(r.content) # convert string to json

		if len(data["results"]) == 0:
			print(address+" (ZERO_RESULTS)")
			continue
		else:
			print(address)

		lat = data["results"][0]["geometry"]["location"]["lat"]
		lng = data["results"][0]["geometry"]["location"]["lng"]

		with open(filePathWithGeo, "a") as myfile:
			myfile.write(str(lat)+","+str(lng)+","+line)

		with open(filePathGeocodesOnly, 'a') as the_file:
			the_file.write(str(data)+"\n")