import requests

url = "https://billboard-api2.p.rapidapi.com/radio-songs"

querystring = {"date":"2024-06-01","range":"1-10"}

headers = {
	"x-rapidapi-key": "350f1485e0mshd0619e3094dbc97p1093b6jsn85015ef157bc",
	"x-rapidapi-host": "billboard-api2.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())