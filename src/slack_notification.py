import json
import requests


def notify(services_status, env, token, triggered_by):
	uri = "https://hooks.slack.com/services/" + token

	response = {
		"text": "Deploying to environment *" + env + "* completed\nJob triggered by *" + triggered_by + "*\n*Deployed services:*",
		"attachments": []
	}

	colors = {
		0: "#6d6c6c",
		4: "#36a64f",
		5: "#ff0000"
	}

	if services_status:
		for service in services_status:
			service_view = {
				"text": service.name,
				"color": colors[service.status]
			}
			response['attachments'].append(service_view)
	else:
		service_view = {
			"text": "No one",
			"color": "#3498db"
		}
		response['attachments'].append(service_view)

	requests.post(uri, data=json.dumps(response))
