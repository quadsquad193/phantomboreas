from phantomboreas import parkinglogservice

import datetime

import sqlalchemy
import config



redis_conf = {
    'host':             config.REDIS_CONN['host'],
    'port':             config.REDIS_CONN['port'],
    'db_index':         config.REDIS_CONN['db_index'],
    'queue_key':        config.REDIS_MQ['parkinglog_queue'],
    'processing_key':   config.REDIS_MQ['parkinglog_processing']
}

db_conf = {
    'db_url':   config.SQLALCHEMY_DATABASE_URI
}

assets_conf = {
    'image_store_path':    config.IMAGE_STORE_PATH
}

rules_conf = {
    'limit': datetime.timedelta(hours=2),
    'grace': datetime.timedelta(minutes=15),
}

parkinglogservice.db.config(db_conf)
parkinglogservice.logger.config(assets_conf)
parkinglogservice.arbiter.config(rules_conf)
parkinglogservice.worker.config(redis_conf)
parkinglogservice.worker.run()
