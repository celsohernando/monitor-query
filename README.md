# Watson IOT Query Service

## What is this?
This is a REST Interface code pattern to demonstrate querying  Watson IOT Maximo Asset Monitor for Entity Type and Entity Data
# The Basics

Use the Maximo Asset Monitor [demo and documentation](https://developer.ibm.com/components/maximo/videos/introducing-ibm-maximo-asset-monitor/) .

Tutorials on REST APIs
https://nikgrozev.com/2018/10/12/python-api-with-flask-and-flask-restplus/
https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html

Watson IOT
DB sdk https://github.com/ibm-watson-iot/functions/blob/development/iotfunctions/db.py
Queries sdk https://github.com/ibm-watson-iot/functions/blob/development/scripts/test_queries.py
Use REST API for Monitor getting Dimensions https://github.com/ibm-watson-iot/functions/blob/1cf584f30ba259ad98b1ca77684c016df9b21748/iotfunctions/db.py#L773


## Clone and download your credentials and they run Flask Python skill.py

###  Setup your Python development environment

1. Install Python https://www.python.org/downloads/
2. Optional [install Git](https://git-scm.com/downloads)
3. Optional install an IDE [Atom](https://atom.io/) or use any text editor
cd into this project's root directory
4. Fork this repository, click the gray Fork button in the top right corner
5. Clone your fork of the boilerplate

* Click the green Clone or download button.
* Copy the https path.
* Using the Terminal
* Git clone git@github.ibm.com:ConsumerIoT/Skill-Boilerplate-Python.git  Replace your forked github url  Skill-Boilerplate-Python.git with your own
```
Git clone git@github.ibm.com:ConsumerIoT/Skill-Boilerplate-Python.git
```
6. Run `pip install -r requirements.txt` to install the app's dependencies

## Setup IBM Cloud service for deploying Cloud Foundry applications

### Setup - the IBM Cloud CLI - Your IBM Cloud org and space do initial push of your skill code to IBM Cloud

1. Create an IBM Cloud [Bluemix Account](https://console.bluemix.net/registration/)
2. Install the [IBM Cloud CLI](https://watson-personal-assistant.github.io/developer/skill/setup-local-dev-env/) if you haven't.   
3. Login to IBM Cloud Bluemix and push the code to IBM Cloud

```
$ bx login -sso
$ bx api https://api.ng.bluemix.net
$ bx target -o "your org" -s "your space"
```
### Prepare & deploy your simulator to the IBM Cloud

1. cd to the project folder expertise-boilerplate-python for your local cloned git python repository
2. Modify the manifest.yml file to replace name and host for "skill-boilerplate-python" with "YourOwnNamePlusYourAge".

```
applications:
- path: .
  memory: 128M
  instances: 1
  domain: mybluemix.net
  name: my-simulator
  host: my-simulator
  disk_quota: 1024M
  buildpack: python_buildpack
```
3. Do and initial push from the terminal window. Don't worry that it won't start initially.  
```
$ bluemix login -sso
$ bluemix target -o "YourOrg" -s "YourSpace"
$ bluemix cf push
$ bluemix app logs "your turbine simulator app name"  --recent  
```

4. Configure required user defined environment variables used to run the simulator.  Add user defined variables below in the deployed IBM Cloud Foundry Application:

* Copy your AS credentials json object into the file credentials_beta-3.json
* Replace the "db" property name with "databaseName" in the postgres section:

```
"databaseName":"ibmclouddb"
```

5. Restart your simulator app so that it will detect your updated user defined environment variables.


## Create your own IBM Maximo Asset Monitor Service
* Directions on how to do this are not covered here.  See the IBM Marketplace for purchasing IBM Maximo Asset Monitor Service.


## Run the REST IOT Query Service on IBM Cloud
* Go to the IBM Cloud Dashboard in a browser https://console.bluemix.net/dashboard/apps

* Make note of your skill URL by pressing on "Visit App URL" in the IBM Cloud Console. Append /v1/api to access your Python Skill Swagger page.
https://yoursimulator.mybluemix.net/v1/api/

## Test the skill running on IBM Cloud directly using the Python Skill  Swagger page
* Access the running skill in a browser at URL: https://turbine-simulator.mybluemix.net/v1/api/
* Press "Try it out! button.
* You should see the simulation data response.
* Review the Response Body. It should look similar to one below.

```
{
}
```

## Configure additionalInformation
Use the URL for your
