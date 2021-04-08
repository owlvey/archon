from datetime import datetime
import os
from flask import Flask
from flask_apscheduler import APScheduler
import logging
import urllib3
from threading import Thread, Lock
from engine.components.ShellComponent import ShellComponent


log_level = os.environ.get("OWLVEY_LOGGING", logging.WARNING)
logging.basicConfig(level=log_level)

class Config(object):
    SCHEDULER_API_ENABLED = True

logger = logging.getLogger()    

app = Flask(__name__)

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()



@scheduler.task('interval', id='sync_job', seconds=120, misfire_grace_time=60)
def sync_job():
    logger.warning('sync_job at {}'.format(datetime.now()))            
    try:
        shell = ShellComponent()
        shell.run()            
        logger.warning('sync_job completed')
    except Exception as e:
        logger.error(e)
    
@scheduler.task('interval', id='health_job', seconds=10, misfire_grace_time=60)
def health_job():
    logger.info('health_job at {}'.format(datetime.now()))            
    try:
        shell = ShellComponent()
        shell.health()            
        logger.info('health_job completed')
    except Exception as e:
        logger.warning(f'health_job error {str(e)}')
        logger.error(e)
    
   

if __name__ == "__main__":     
    value = os.environ.get("OWLVEY_CONFIG")
    logger.warning(f"\n ** OWLVEY_CONFIG : {value}")
    app.run(host='0.0.0.0', port=50001)