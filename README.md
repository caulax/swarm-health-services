# Determine deployed service in Docker Swarm with Slack notification

## Features 
* Recognize working services
* Start update services by custom command
* Determine what services were updated
* Push notification to Slack

## Run on host

### Install python2.7 and pip
<https://pip.pypa.io/en/stable/installing/>

### Install dependencies
`pip install --no-cache-dir -r requirements.txt`  

### Run
`python main.py --help`  

## Build and run in docker 
`docker build -t swarm-updated-service .`  
`docker run --rm swarm-updated-service python main.py --help`

### Example run
`python main.py -u USERNAME_TRIGGED_BY -st SLACK_TOKEN -e ENV -pn PROJECT_NAME -c COMMAND1 -c COMMAND2`  
_-u - username who started deploy_  
_-st - token for Slack App_  
_-e - environment where deploy was started_  
_-pn - project name_  
_-c - commands to deploy_  
_*All parameters are required_ 
