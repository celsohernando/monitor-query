#--------------------------------------------------------------------------------
# These tokens are needed for user authentication.
# Credentials can be generates via Twitter's Application Management:
#	https://apps.twitter.com/app/new
#--------------------------------------------------------------------------------

# settings.py
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity:
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only


# If on bluemix load env differently
# Load Environment variables set via VCAP variables in Bluemix
if 'VCAP_SERVICES' in os.environ:
    print("On Bluemix...")

# Load Environment Variables in a sane non Bluemix way
else:
    print("Not On Bluemix...")
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)



ACCESS_KEY = os.getenv("ACCESS_KEY")
logger.debug('ACCESS_KEY %s' %ACCESS_KEY )
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
logger.debug('ACCESS_SECRET %s' %ACCESS_SECRET )
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
logger.debug('CONSUMER_KEY %s' %CONSUMER_KEY )
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
logger.debug('CONSUMER_SECRET %s' %CONSUMER_SECRET )
ACCESS_KEY = os.getenv("ACCESS_KEY")
A101FLATLINE_TEMP = os.getenv("A101FLATLINE_TEMP")
logger.debug('A101FLATLINE_TEMP %s' %A101FLATLINE_TEMP )
A101FLATLINE_TIME = os.getenv("A101FLATLINE_TIME")
logger.debug('A101FLATLINE_TIME %s' %A101FLATLINE_TIME )
A101_INDEX = os.getenv("A101_INDEX")
logger.debug('A101_INDEX %s' %A101_INDEX )

# ANomaly Temp
def setenv_temp( env_temp ):
    logger.debug("Check setenv_temp input temp %s "  %env_temp)
    os.environ["A101FLATLINE_TEMP"] = env_temp
    A101FLATLINE_TEMP = os.environ["A101FLATLINE_TEMP"]
    logger.debug("Check that flatline A101FLATLINE_TEMP was set in settings %s "  %A101FLATLINE_TEMP)
    return

def getenv_temp():
    A101FLATLINE_TEMP = os.environ["A101FLATLINE_TEMP"]
    logger.debug("getenv_temp  A101FLATLINE_TEMP %s "  %A101FLATLINE_TEMP)
    return A101FLATLINE_TEMP

#Anomaly Time
def setenv_time( env_time ):
    logger.debug("Check setenv_temp input env_time %s "  %env_time)
    if env_time == None:
        os.environ["A101FLATLINE_TIME"] = "None"
    else:
        os.environ["A101FLATLINE_TIME"] = env_time
    A101FLATLINE_TIME = os.environ["A101FLATLINE_TIME"]
    logger.debug("Check that flatline A101FLATLINE_TIME was set in settings %s "  %A101FLATLINE_TIME)
    return

def getenv_time():
    A101FLATLINE_TIME = os.environ["A101FLATLINE_TIME"]
    logger.debug("getenv_time  A101FLATLINE_TIME %s "  %A101FLATLINE_TIME)
    return A101FLATLINE_TIME


def setenv_index( env_index ):
    logger.debug("Incremented A101_INDEX" )
    logger.debug(  env_index )
    os.environ["A101_INDEX"] =  str(env_index)
    A101_INDEX = os.getenv("A101_INDEX")
    logger.debug("Incremented Final A101_INDEX ")
    logger.debug( A101_INDEX )
    return

def getenv_index():
    A101_INDEX = os.environ["A101_INDEX"]
    logger.debug("getenv_index  A101_INDEX %s "  %A101_INDEX )
    return A101_INDEX
