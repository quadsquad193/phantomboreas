__all__ = ['worker', 'logger']

from parkinglogservice.worker import Worker
from parkinglogservice.logger import Logger
logger = Logger()
worker = Worker(logger)
