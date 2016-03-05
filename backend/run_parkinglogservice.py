import parkinglogservice
import config



redis_conf = {
    'host':             config.REDIS_CONN['host'],
    'port':             config.REDIS_CONN['port'],
    'queue_key':        config.REDIS_MQ['parkinglog_queue'],
    'processing_key':   config.REDIS_MQ['parkinglog_processing']
}

db_conf = {

}

parkinglogservice.logger.config(db_conf)
parkinglogservice.worker.config(redis_conf)
parkinglogservice.worker.run()
