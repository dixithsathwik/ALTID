import os
import logging

# JWT Configuration
JWT_EXPIRATION_MINUTES = 15
JWT_ISSUER = 'AltID'
# Default claims that will be overridden during verification
JWT_CLAIMS = {
    'age_verified': False  # This will be updated during verification
}

# Age Verification
MINIMUM_AGE = 18  # Minimum required age in years

# Logging Configuration
LOG_FAILED_ATTEMPTS = True
LOG_LEVEL = logging.INFO  # Set to DEBUG for more verbose logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

# Clear any existing handlers
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Create file handler which logs even debug messages
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(LOG_LEVEL)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# Create formatter and add it to the handlers
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the root logger
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info(f"Logging initialized. Log file: {log_file}")
LOG_FILE = 'verification_failures.log'