__all__ = ['worker', 'logger']

from worker import Worker
from logger import Logger
logger = Logger()
worker = Worker(logger)
