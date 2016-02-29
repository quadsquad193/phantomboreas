import openalprservice
import config

redis_conf = {
    'host':             config.REDIS_CONN['host'],
    'port':             config.REDIS_CONN['port'],
    'queue_key':        config.REDIS_MQ['openalpr_queue'],
    'processing_key':   config.REDIS_MQ['openalpr_processing']
}

openalpr_conf = {
    'country':      config.OPENALPR['country'],
    'region':       config.OPENALPR['region'],
    'config_file':  config.OPENALPR['config_file'],
    'runtime_dir':  config.OPENALPR['runtime_dir']
}

openalprservice.worker.config(redis_conf, openalpr_conf)
openalprservice.worker.run()
