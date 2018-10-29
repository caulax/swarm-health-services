import docker_services
# import check_image
import slack_notification
import argparse


def run(args):
	running_service = docker_services.get_services_and_images_by_project_name(args.project_name)

	if running_service:
		time = docker_services.update_services(args.commands)
		updated_service = docker_services.get_updated_services(running_service, time)
		# check_image.push(updated_service)
		deployed = docker_services.check_deployed_services(updated_service)
		if args.slack_token:
			slack_notification.notify(deployed, args.env, args.slack_token, args.user_triggered)
	else:
		print "No services"


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-pn", "--project-name", help="actions: create, accept MR or new tag", dest="project_name", type=str, required=True)
	parser.add_argument("-st", "--slack-token", help="slack token for ", dest="slack_token", type=str, required=False)
	parser.add_argument("-u", "--user-triggered", help="user how triggered job", dest="user_triggered", type=str, required=False)
	parser.add_argument("-e", "--env", help="environment for project", dest="env", type=str, required=True)
	parser.add_argument("-c", "--command", help="commands to execute", dest="commands", type=str, required=True, action="append")
	parser.set_defaults(func=run)
	args = parser.parse_args()
	args.func(args)


if __name__ == "__main__":
	main()
