import json
import requests


def push(services, service_url):
	json_services = []
	for s in services:
		json_services.append(json.dumps(s.__dict__))
	requests.post(service_url, json=json.dumps(json_services))

	return json.dumps(json_services)
