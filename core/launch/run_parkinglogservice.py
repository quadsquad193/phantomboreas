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
    'timedelta_limit':  datetime.timedelta(hours=2),
    'timedelta_hot':    datetime.timedelta(minutes=15),
    'time_start':       datetime.time(hour=8),
    'time_end':         datetime.time(hour=12+6),
    'days_enforced':    {
        'sunday':       True,
        'monday':       True,
        'tuesday':      True,
        'wednesday':    True,
        'thursday':     True,
        'friday':       True,
        'saturday':     False,
    },
    'gps_proximity': 0.00009 * 25,  # 0.00009 ~= 1 meter
}

parkinglogservice.db.config(db_conf)
parkinglogservice.logger.config(assets_conf)
parkinglogservice.arbiter.config(rules_conf)
parkinglogservice.worker.config(redis_conf)
parkinglogservice.worker.run()
