JWT_EXPIRATION_MINUTES = 15
JWT_ISSUER = 'AltID'
JWT_CLAIMS = {
    'age_verified': True,  # Default claim, can be customized per user
}
LOG_FAILED_ATTEMPTS = True
LOG_FILE = 'verification_failures.log' 