import datetime as dt
import json
import logging
import urllib3
# from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from iotfunctions.db import Database
from iotfunctions.enginelog import EngineLogging
import settings

EngineLogging.configure_console_logging(logging.DEBUG)


class IotEntityType(object):
    '''
    Query Entity objects
    Parameters:
    -----------
    credentials: dict
        Maximo Asset Monitor credentials.
    entity_type_name: string
        Entity Type name to get the entities for.
    echo: bool
        Output sql to log
    '''

    def __init__(self, entity_type_name=None):
        self.entity_type_name = entity_type_name
        logging.info(self.entity_type_name)
        self.db_schema = "BLUADMIN"  # only required if you are not using the default
        # self.table_name =  entity_type_name.upper()  # change to a valid entity time series table name
        # self.dim_table_name = "DM_"+self.table_name  # change to a entity dimenstion table name
        # self.timestamp = 'evt_timestamp'
        self.credentials = settings.CREDENTIALS
        # logging.info('username %s' %self.credentials['db2']['username'])
        # logging.info('password %s' %self.credentials['db2']['password'])
        # logging.info('host %s' %self.credentials['db2']['host'])
        # logging.info('port %s' %self.credentials['db2']['port'])
        # logging.info('databaseName%s' %self.credentials['db2']['databaseName'])
        self.db = Database(credentials=self.credentials)
        self.entity_names = self.get_entity_names
        if entity_type_name != None:
            self.table_name = entity_type_name.upper()  # change to a valid entity time series table name
            self.dim_table_name = "DM_" + self.table_name  # change to a entity dimenstion table name
        self.timestamp = 'evt_timestamp'
        self.http = urllib3.PoolManager()

    # Works
    def get_entity_names(self):
        logging.info("get_entity types")
        entity_names_list = []
        # Retrieve entity_types
        # logging.info("get_entity_types metadata %s" % self.db.entity_type_metadata)
        for item in self.db.entity_type_metadata:
            logging.info("item %s" % item)
            entity_names_list.append(item)
        self.entity_names = entity_names_list
        return (entity_names_list)

    def get_entity_type_dimensions(self, entitytype=None):
        logging.info("get_entity_type_dimensions %s " % entitytype)
        dimensions_list = []
        # Call HTTP REST Service using: https://urllib3.readthedocs.io/en/latest/user-guide.html
        # https://api-beta.connectedproducts.internetofthings.ibmcloud.com/api/master/v1/Monitor-Demo/entity/type/Clients04/categorical
        # payload = ''
        # encoded_payload = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': "application/json", 'x-api-key': self.credentials['iotp']['apiKey'],
                   'x-api-token': self.credentials['iotp']['apiToken'], }
        try:
            url = 'https://api-beta.connectedproducts.internetofthings.ibmcloud.com/api/master/v1/Monitor-Demo/entity/type/' + entitytype + '/categorical'
        except KeyError:
            raise ValueError(('This combination  of request_type (%s) and'
                              ' object_type (%s) is not supported by the'
                              ' python api') % (object_type, request))

        r = self.http.request("GET", url, body="", headers=headers)
        logging.info("get_entity_type_dimensions response %s" % r.status)
        # response = r.data.decode('utf-8')

        if r.status == 401:
            logging.info("get_entity_type_dimensions not found on this entity.")
            response = {"None": "None"}
        else:
            # if response.status_code >= 300 or response.status_code < 200:
            response = json.loads(r.data.decode('utf-8'))
            logging.info("get_entity_type_dimensions response %s" % response)
            for item in response:
                logging.info("dimensions item %s" % item)
                dimensions_list.append(item)
            self.dimensions = dimensions_list
        return (response)

    # Works
    def get_entity_type_metadata(self, entity_type=None):
        logging.info("get_entities for entity_type %s" % entity_type)
        try:
            metadata = self.db.entity_type_metadata[entity_type]
            logging.info("get_entities metadata %s" % metadata)
        except KeyError:
            logging.info("get_entities metadata failed")
        '''
        logging.info("get_entities ids for entity_type" )
        try:
            entity_type_id = metadata.get('entityTypeId', None)
            logging.info("Entities entity_type_id found is %s" % entity_type_id)
            entity_id = metadata.get('ID', None)
            logging.info("Entities entity_id found is %s" %entity_id)
        except TypeError:
            logging.info("Entities not found in the database metadata")
        '''
        return (metadata)

class IotEntity(object):
    '''
    Query Entity objects to establish Events Streams connectivity, manage Stream metadata and sessions
    Parameters:
    -----------
    credentials: dict (optional)
        Database credentials. If none specified use DB_CONNECTION_STRING environment variable
    start_session: bool
        Start a session when establishing connection
    echo: bool
        Output sql to log
    '''

    def __init__(self, entity_type_name=None, entity_name=None ):
        # replace with valid table and column names
        self.entity_type_name = entity_type_name
        self.entity_name = entity_name
        self.db_schema = "BLUADMIN"  # only required if you are not using the default
        self.table_name =  entity_type_name.upper()  # change to a valid entity time series table name
        self.dim_table_name = "DM_"+self.table_name  # change to a entity dimenstion table name
        self.timestamp = 'evt_timestamp'
        self.credentials = settings.CREDENTIALS
        # logging.info('username %s' %self.credentials['db2']['username'])
        # logging.info('password %s' %self.credentials['db2']['password'])
        # logging.info('host %s' %self.credentials['db2']['host'])
        # logging.info('port %s' %self.credentials['db2']['port'])
        # logging.info('databaseName%s' %self.credentials['db2']['databaseName'])
        self.db = Database(credentials=self.credentials)

    def query(self, metrics=None, timestamp='evt_timestamp', agg_dict=None, to_csv=True):
        logging.info("Query %s and output format is %s" %(agg_dict, to_csv) )
        # Retrieve a single data item using a standard aggregation function
        #agg = {metrics[0]: ['mean']}
        df = self.db.read_agg(table_name=self.table_name, schema=self.db_schema, timestamp='evt_timestamp', agg_dict=agg, to_csv=to_csv)
        return(df)

    # Works
    def query_entity_data(self, columns=None,
                          start_ts=None,
                          end_ts=None):
        '''
        Read whole table and return chosen metrics for selected start and end time as a dataframe
        Parameters
        -----------
        table_name: str
            Source table name
        schema: str
            Schema name where table is located
        columns: list of strs
            Projection list
        timestamp_col: str
            Name of timestamp column in the table. Required for time filters.
        start_ts: datetime
            Retrieve data from this date
        end_ts: datetime
            Retrieve data up until date
        entities: list of strs
            Retrieve data for a list of deviceids
        dimension: str
            Table name for dimension table. Dimension table will be joined on deviceid.
        parse_dates: list of strs
            Column names to parse as dates
        '''
        logging.info('table_name %s' %self.table_name)
        logging.info('db_schema %s' %self.db_schema)
        columns.append("RCV_TIMESTAMP_UTC")
        logging.info('columns %s' %columns)
        df = self.db.read_table(table_name="IOT_" + self.table_name,
                                schema=self.db_schema,
                                parse_dates=None,
                                columns=columns,
                                timestamp_col='RCV_TIMESTAMP_UTC',
                                start_ts=start_ts,
                                end_ts=end_ts)
        logging.info(df)
        query_data = df.to_json()
        return query_data

if __name__ == "__main__":

    #iot_entity_type = IotEntityType(entity_type_name = "Clients04")
    #logging.info("get_entity_types(self) %s " %iot_entity_type.get_entity_names())
    #logging.info("get_entities(self) %s " % iot_entity_type.get_entity_type_metadata("Clients04"))
    #logging.info("get_entities(self) %s " %iot_entity_type.get_entity_type_dimensions(entitytype="cc3200LP"))
    now = dt.datetime.utcnow()
    start_ts="2019-12-07 10:34:24.198099"
    query_data = IotEntity(entity_type_name="IOT_CC3200LP", entity_name="2117").query_entity_data( columns=["Temperature"],
                                                                                       start_ts=start_ts,
                                                                                       end_ts=now)
    '''
        {
          "entitytype": "cc3200LP",
          "entity": "Blower-North",
          "start_ts": "2019-12-06 11:43:49.125735",
          "end_ts": "Now",
          "columns": [
            "Temperature"
          ]
        }
    iot_entity_type = IotEntityType(entity_type_name = "cc3200LP")
    logging.info("get_entity_types(self) %s " %iot_entity_type.get_entity_names())
    logging.info("get meta_data and entities  %s " % iot_entity_type.get_entity_type_metadata("cc3200LP"))
    logging.info("get_entities(self) %s " %iot_entity_type.get_entity_type_dimensions(entitytype="Blower-North"))
    now = dt.datetime.utcnow()
    start_ts="2019-12-07 10:34:24.198099"
    query_data = IotEntity(entity_type_name="cc3200LP", entity_name="Blower-North").query_entity_data( columns=["Temperature"],
                                                                                        start_ts=start_ts,
                                                                                        end_ts=now)
    '''

