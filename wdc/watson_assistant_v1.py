###
# Copyright 2017 IBM All Rights Reserved.
###
from wdc_service import WatsonDeveloperCloudService
import sys
import logging
import os
import json
#from watson_developer_cloud.conversation_v1 import Context
from flask import request
#logger.basicConfig(level=logging.INFO)
#logger.basicConfig( level=logger.debug)
logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

class Handler(WatsonDeveloperCloudService):
    #  Handles request from the Watson Assistant Core Service so that it an call Watson Conversation Service
    #default_url = 'http://carloshelloskill.mybluemix.net/'
    version = '2018-02-16'
    platform_url = 'https://gateway.watsonplatform.net'
    service_path = '/conversation/api'
    base_url = '{0}{1}'.format(platform_url, service_path)
    workspace_id = None

    def __init__(self, version=version, url=base_url, username=None, password=None):
        # Construct an instance. Fetches service parameters from VCAP_SERVICES
        # runtime variable for Bluemix, or it defaults to local URLs.
        # :param version: specifies the specific version-date of the service to
        # use :
        # Twitter Alerts Workspace
        # CMFConversation instance
        # workspace_id ='3a0fc69d-ec30-4d43-a18e-91db3c25a902'

        logger.debug('Class Handler - init -----------------------')
