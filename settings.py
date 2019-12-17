import os
import json
import logging
from dotenv import load_dotenv
from os.path import join, dirname


def set_log_level(logger_level):
    logging.getLogger().setLevel(logger_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logger_level)

    # create formatter
    formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - \n%(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logging.getLogger().addHandler(ch)


# Configure Logging Default
set_log_level(logging.INFO)

# Determine where running and load credentials
if 'VCAP_APPLICATION' in os.environ:
    # Running on BLuemix load credentials from VCAP Services.
    print("On Bluemix...")
    vcap_application = json.loads(os.environ.get('VCAP_APPLICATION'))
    logging.info('vcap_services: %s ' %vcap_application)
    logging.info('Credentials user defined env var before %s ' %os.getenv("CREDENTIALS"))
    CREDENTIALS = json.loads( os.getenv("CREDENTIALS") )
    logging.info('Credentials after %s ' %CREDENTIALS)
else:
    # Running local and get credentials from the json file passed in.

    # Check for existance of .env file
    env_path = join(dirname(__file__), '.env')

    # Load .env file into os.environ
    #load_dotenv(env_path)

    # ===================
    # Load credentials.json file that has been downloaded from Monitor Usage tab
    # credentials_Monitor-Demo
    # or
    # credentials_beta-3 - Demo
    # ===================
    try:
        with open('credentials_beta-3.json', encoding='utf-8') as F:
            logging.info('Running Local Credentials user defined env var before %s ' %F.read())
        with open('credentials_beta-3.json', encoding='utf-8') as F:
            CREDENTIALS = json.loads(F.read())
            logging.info('Running Local Credentials after %s ' %CREDENTIALS)
    except Exception as ex:
        logging.info('Exception Credentials %s ' %CREDENTIALS)
        template = 'Error: {0} Problem reading Consumer Settings credentials or urls from environment variables.: \n{1!r}'
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)