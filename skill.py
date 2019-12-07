###
# Copyright 2019 Carlos Ferreira All Rights Reserved.
###
from flask import Flask, request, Blueprint
from flask import jsonify
from flask_restplus import Resource, fields, Api, reqparse, marshal
from werkzeug.contrib.fixers import ProxyFix
import logging
#from wdc.watson_assistant_swagger import SkillSwagger
import os, json
from query import IotEntity, IotEntityType
import datetime as dt
from time import gmtime, strftime
import settings
import random
import numpy as np

#help curl --help
app = Flask(__name__, static_folder='static')
app.wsgi_app = ProxyFix(app.wsgi_app)
port =  os.getenv('PORT', '5000')
app.logger.addHandler(logging.StreamHandler())
#app.logger.setLevel(logging.INFO)
app.logger.setLevel(logging.DEBUG)
#app.logger.info('XXXXXXXXXXXXXXXXXXXXXXXX - Get port %s ' %port)

###
# Sets up SWAGGER documentation to allow you to see format of JSON to input to try the service.
###
api_v1 = Blueprint('api', __name__, url_prefix='/v1/api')
app.logger.debug('Created Blueprint ')

api = Api(api_v1, name="SkillAPI", version='1.0', title='IOT Query Service',
    description='Allows you to qyery timeseries data of IOT Devices in Maximo Asset Monitor',)
app.logger.debug('Created API ')

manifest_input = api.model('manifest', {"manifest" :{}
})

user_data = api.model('user_data', {
  'id': fields.String(readOnly=True, description='The task unique identifier'),
})

session_data = api.model('session_data', {
    'id': fields.String(readOnly=True, description='The task unique identifier'),
    'new': fields.Boolean(required=False, description='This is a new session'),
    'attributes': fields.String(required=True, description='JSON'),
    'version': fields.String(required=True, version='0.0.1'),
})

application_data = api.model('application_data', {
  'id': fields.String(readOnly=True, description='The task unique identifier'),
  'attributes': fields.String(required=True, description='attributes JSON'),
})

context_data = api.model('context_data', {
  'user': fields.Nested(user_data),
  'session': fields.Nested(session_data),
  'application': fields.Nested(application_data),
})

query_entity_data_input_data = api.model('query_entity_data_input_data', {
    'entitytype': fields.String(required=True, description='Entity Type'),
    'entity': fields.String(required=True, description='Entity'),
    'start_ts': fields.String(required=True, description='Stat Time Stamp format 2019-12-06 11:43:49.125735 '),
    'end_ts': fields.String(required=True, description='End Time Stamp enter "Now" for now.'),
    'columns': fields.List(fields.String(required=True, description='The list of columns')),
})

get_entity_type_dimensions_input_data = api.model('get_entity_type_dimensions_input_data', {
    'entitytype': fields.String(required=True, description='Entity Type'),
})

get_entity_type_metadata_input_data = api.model('get_entity_type_metadata_input_data', {
    'entity_type': fields.String(required=True, description='The Entity Type you want to get the Entity Metadata for.'),
})

manifest = api.model('Manifest', {
  'name': fields.String(required=True, description='The skill name'),
  'description': fields.String(required=True, description='A description of what the skill does'),
  'private': fields.Boolean(required=False, description='Set false to make the skill discoverable'),
  'author': fields.String(required=True, author='The business or technical owner'),
  'version': fields.String(required=True, version='0.0.1'),
  'license': fields.String(required=True, description='For example: Apache-2.0'),
  'callword': fields.String(required=True, description='How to call this skill by name'),
  'lifetime': fields.String(required=True, description='lifetime'),
  'threshold': fields.Float(required=True, description='0.85'),
  'languages': fields.List(fields.String),
  #'nlu': fields.String(required=True, description='"nlu": ["regexp"]'),
  'tags': fields.List(fields.String),
  'nlu': fields.List(fields.String),
  'services': fields.List(fields.String),
  })

workspace_data = api.model('workspace_data', {
  'en-US': fields.Nested(
                    api.model('Name',
                            { 'name': fields.String(required=True, description='restaurant-en') }
                            )
            )
})

#workspace_data = api.model( { fields.List(fields.Nested(language_data) )
#})

credentials_data = api.model('credentials_data',{
                                'version': fields.String( required=False, description='Version' ) ,
                                'version_date': fields.Date( required=False, description='Date 2016-09-27' ) ,
                                'password': fields.String( required=False, description='Password' ) ,
                                'username': fields.String( required=False, description='Username' ),
})

nlu = api.model('NLU', {
  'workspace' : fields.Nested(workspace_data),
  'credentials' : fields.Nested(credentials_data),
})


entities =  api.model('Entities', {
    'entities' : fields.Nested(
                    api.model('Name',
                                { "name" : fields.String( required=False, description='Entity name' ) ,
                                 'required': fields.Boolean( required=False, description='Required or not. Boolean' )
                                 }
                    )
                )
    }
)

intents = api.model('Intents', {
  'visibility' : fields.Boolean( required=False, description='visibility. value = always' ) ,
  'entities' : fields.Nested(entities),
})


###
# Business Logic that retrieves your skill data via methods that will be used by the get, put, post and delete in Swagger Classes below.
###
class WatsonIot(object):
    def __init__(self):
        app.logger.debug('Intitialize WatsonIot ')

    ###
    # Get Entity Type Dimensions
    ###
    def get_entity_type_dimensions(self,request):
        app.logger.info('get_entity_type_dimensions------- ')
        try:
            entitytype = request.json['entitytype']
            app.logger.debug('query -  entitytype %s' % entitytype)
        except KeyError as inst:
            app.logger.debug('query - Wrong input provided')
        try:
            iot_entity_type = IotEntityType()
            entity_type_dimensions = iot_entity_type.get_entity_type_dimensions(entitytype=entitytype)
            logging.info("get entity_type_dimensions %s " %entity_type_dimensions)
        except KeyError as inst:
            app.logger.debug('get_entity_type_dimensions method - problems accessing Service')
        response_back = { "data" : None,
                        "responseCode": 200,
                        "requestResult": "Done",
                        }
        response_back['data'] = entity_type_dimensions
        return response_back

    ###
    # Get Entity Types
    ###
    def get_entity_types(self,request):
        app.logger.debug('class WatsonIOT , get_entity_types method -------')
        try:
            iot_entity_type = IotEntityType()
            entity_types_data = iot_entity_type.get_entity_types()
            logging.info("get_entity_types(self)")
        except KeyError as inst:
            app.logger.debug('get_entity_types method - problems accessing Service')
        response_back = { "data" : None,
                        "responseCode": 200,
                        "requestResult": "Done",
                        }
        response_back['data'] = entity_types_data
        return response_back

    ###
    # Get Entity Type Metadata like what columns and metrics the Entity Type has
    ###

    def get_entity_type_metadata(self, request):
        app.logger.debug('class WatsonIOT , get_entity_type_metadata method -------')
        try:
            entitytype = request.json['entitytype']
            app.logger.debug('query -  entitytype %s' % entitytype)
        except KeyError as inst:
            app.logger.debug('query - Wrong input provided')
        iot_entity_type = IotEntityType()
        entity_type_metadata = iot_entity_type.get_entity_type_metadata(entitytype)
        logging.info("entity_type_metadata %s " %entity_type_metadata)
        response_back = {"data": None,
                         "responseCode": 200,
                         "requestResult": "Done",
                         }
        response_back['data'] = entity_type_metadata
        return response_back

    ###
    # Get Entities given an Entity Type
    ###
    def get_entities(self,request):
        app.logger.debug('class WatsonIOT , get_entities method -------')
        try:
            entity_type = request.json['entitytype']
            app.logger.debug('query -  entitytype %s' % entity_type)
        except KeyError as inst:
            app.logger.debug('query - Wrong input provided')

        entities_data = IotEntity(entity_type_name=entity_type, entity_name=entity_name).query_entity_data(columns=entity_columns,
                                                                                                           start_ts=start_ts,
                                                                                                           end_ts=end_ts)
        response_back = { "data" : None,
                        "responseCode": 200,
                        "requestResult": "Done",
                        }
        response_back['data'] = json.loads(entities_data)
        return response_back

    ###
    # Query Maximo Asset Monitor
    ###
    def query_entity_data(self, request):
        app.logger.debug('class WatsonIOT , query method -------%s' %request.json['entitytype'])

        ###
        # Retrieve request Query Parameters for Entity Type, Entity and Columns
        # Columns = ["EVT_TIMESTAMP", "TEMPERATURE"]
        ###
        start_ts = None
        end_ts = None
        try:
            entity_type = request.json['entitytype']
            app.logger.debug('query -  entitytype %s' %entity_type)
            entity_name = request.json['entity']
            app.logger.debug('query -  entity %s' %entity_name)
            start_ts = request.json['start_ts']
            app.logger.debug('query -  start_ts %s' % start_ts)
            end_ts = request.json['end_ts']
            app.logger.debug('query -  end_ts %s' % end_ts)
            entity_columns = request.json['columns']
            app.logger.debug('query -  columns %s' %entity_columns)
        except KeyError as inst:
            app.logger.debug('query - Wrong input provided')
        if end_ts == "Now":
            end_ts = dt.datetime.utcnow()
        query_data = IotEntity(entity_type_name=entity_type, entity_name=entity_name).query_entity_data(columns=entity_columns,
                                                                                                        start_ts=start_ts,
                                                                                                        end_ts=end_ts)
        response_back = { "data" : None,
                        "responseCode": 200,
                        "requestResult": "Done",
                        }
        response_back['data'] = json.loads(query_data)
        return response_back

    def manifest(self,request):
        app.logger.debug('class WatsonAssistant - Entereed manifest method in welcome and Arg ID -------')
        # Chck if response from conversation service cntx with this user has location and category exist
        response_back = {
          "responseCode": 200,
          "requestResult": "Done",
          }
        return response_back

    def nlu(self,request):
        # Chck if response from conversation service cntx with this user has location and category exist
        response_back = {
          "responseCode": 200,
          "requestResult": "Done",
          }
        return response_back
    def intents(self,request):
        # Chck if response from conversation service cntx with this user has location and category exist
        response_back = {
          "responseCode": 200,
          "requestResult": "Done",
          }
        return response_back

rest_api = WatsonIot()

@api.route('/manifest')
class Manifest(Resource):
    # @api.expect(manifest_input)
    # curl http://localhost:5000/manifest
    def get(self, **kwargs):
        app.logger.debug('class Manifest Resource ----------------------')
        app.logger.debug('class Manifest Resource Method get, returning WPASkill.manifest')
        return rest_api.manifest(request), 201

@api.route('/query_entity_data')
class Query_Entity_Data(Resource):
    @api.expect(query_entity_data_input_data)
    def post(self, **kwargs):
        app.logger.debug('class query_entity_data  Resource ----------------------')
        app.logger.debug(json.dumps(request.json, indent=2))
        return rest_api.query_entity_data(request), 201

@app.route('/queryFile', methods=['POST'])
class QueryFile(Resource):
    def post(self, **kwargs):
        app.logger.debug('QueryFile')
        content = str(request.form['jsonval'])
        return rest_api.query_entity_data(request,
                                          mimetype='application/json',
                                          headers={'Content-Disposition': 'attachment;filename=zones.geojson'})

@api.route('/get_entity_types')
class Get_Entity_Types(Resource):
    app.logger.debug('class Get_Entity_Types Resource ----------------------')
    def get(self, **kwargs):
        return rest_api.get_entity_types(request), 201

@api.route('/intents')
class Intents(Resource):
    def get(self, **kwargs):
        app.logger.debug('class Intents Resource  api route----------------------')
        # curl http://127.0.0.1:5000/v1/api/intents
        return rest_api.intents(request), 201

@api.route('/get_entity_type_dimensions')
class Get_Entity_Type_Dimensions(Resource):
    @api.expect(get_entity_type_dimensions_input_data)
    def post(self, **kwargs):
        app.logger.debug('get_entity_type_dimensions - --- request from IOT Query Service -start')
        app.logger.debug(json.dumps(request.json, indent=2))
        app.logger.info('get_entity_type_dimensions - --- request from Watson Assistant Solutions Core Service -finish')
        return rest_api.get_entity_type_dimensions(request), 201

@api.route('/get_entity_type_metadata')
class Get_Entity_Type_Metadata(Resource):
    @api.expect(get_entity_type_metadata_input_data)
    def post(self, **kwargs):
        app.logger.debug('class get_entity_type_metadata Resource  api route----------------------')
        app.logger.debug(json.dumps(request.json, indent=2))
        # curl http://127.0.0.1:5000/v1/api/get_entity_type_metadata
        return rest_api.get_entity_type_metadata(request), 201

if __name__ == '__main__':
    app.register_blueprint(api_v1)
    #Uncomment next line to debug loccally then $python skill.py in terminal
    app.run(debug=True)
    #Uncomment next line to run on bluemix.
    #app.run(host='0.0.0.0', port=int(port))
