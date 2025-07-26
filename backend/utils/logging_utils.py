import logging
import os
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_failure(reason, details=None):
    msg = f"Failure: {reason}"
    if details:
        msg += f" | Details: {details}"
    logging.info(msg) 