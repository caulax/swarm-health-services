import docker
import os
import json
import time
from Service import Service


FOUND = 0
RUNNING = 1
NEW_IMAGE = 2
UPDATING = 3
COMPLETED = 4
UNKNOWN = 5


def update_services(commands):
	time_start_deploy = time.time()
	for command in commands:
		os.system(command)
	return time_start_deploy


def get_updated_services(services, start_time_deploy):
	client = docker.from_env()

	events_filter = {
		'type': 'service'
	}

	for event in client.events(since=start_time_deploy, filters=events_filter):
		dict_event = json.loads(event)
		events_attributes = dict_event['Actor']['Attributes']

		for service in services:
			if events_attributes['name'] in service.name:
				service.status = RUNNING
				if ('image.new' in events_attributes):
					service.set_new_image(events_attributes['image.new'])
					service.status = NEW_IMAGE
				if ('updatestate.new' in events_attributes and events_attributes['updatestate.new'] == 'updating'):
					service.status = UPDATING
				if ('updatestate.new' in events_attributes and events_attributes['updatestate.new'] == 'completed'):
					service.status = COMPLETED
				if ('updatestate.new' in events_attributes) and \
					(events_attributes['updatestate.new'] == 'paused' or events_attributes['updatestate.new'] == 'unknown'):
					service.status = UNKNOWN
		if check_status_services(services):
			return services


def check_status_services(services):
	status_list = []
	for service in services:
		status_list.append(service.status)
	if UPDATING in status_list or FOUND in status_list or NEW_IMAGE in status_list:
		return False
	else:
		return True


def check_deployed_services(services):
	services_deployed = []
	for service in services:
		if service.status != RUNNING:
			services_deployed.append(service)
	return services_deployed


def get_services_and_images_by_project_name(name):
	client = docker.from_env()

	services_filter = {
		'name': name
	}
	tasks_filter = {
		'desired-state': 'running'
	}

	services = []

	running_services = client.services.list(filters=services_filter)

	for s in running_services:
		service = Service(name=s.name, status=FOUND)
		tasks = s.tasks(filters=tasks_filter)
		if (tasks):
			for t in tasks:
				service.set_image(t['Spec']['ContainerSpec']['Image'])
		services.append(service)
	return services
