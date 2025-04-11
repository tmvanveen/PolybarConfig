#!/usr/bin/env python3

from requests import get

url = "http://192.168.1.100:8123/api/states/sensor.co2_beneden"
headers = {
	"Authorization": "Bearer oMfqBWIpcm7PBDG1IJzI1EckqwlkpscrIiHNKbFs7o",
	"content-type": "application/json",
}

response = get(url, headers=headers)

data = response.json()

CO2Waarde = data['state']
CO2Eenheid = data['attributes']['unit_of_measurement']

print(CO2Waarde,CO2Eenheid)
