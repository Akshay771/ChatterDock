import os

# temp folder
TEMP_FOLDER_PATH = '/app/temp'

# allowed extensions
ALLOWED_EXTENSIONS = ['csv', 'xls', 'xlsx', 'txt', 'pdf', 'mp4', 'png', 'jpeg', 'jpg', 'mp3', 'mpeg', 'mpg', 'doc',
                      'docx', 'webp', 'heic', 'HEIC']

# Base URL
# BASE_URL = "https://medisetter.com"  # will work only when UI page to set password is complete
REACT_APP_BASE_URL = os.environ.get('REACT_APP_BASE_URL')

# API Success/Failure Messages
API_SUCCESS_STATUS = 'Success'
API_FAILURE_STATUS = 'Failure'
API_ERROR_STATUS = 'Error'

# Template types
TEMPLATE_TYPE_EMAIL = 'email'

# PRIVATE KEY GCP
PRIVATE_KEY = ("")

# Roles
ADMIN_ROLE = 'ADMIN'
CO_ADMIN_ROLE = 'CO-ADMIN'
USER_ROLE = 'USER'
# GCP
GCP_URL_VALIDITY = 15  # minutes


# User Status
PENDING_STATUS = 'PENDING'
APPROVED_STATUS = 'APPROVED'
REJECTED_STATUS = 'REJECTED'
PARTIALLY_APPROVED_STATUS = 'PARTIALLY_APPROVED'
DISABLED_STATUS = 'DISABLED'
DEACTIVATED_STATUS = 'DEACTIVATED'

# Bucket access
PUBLIC_BUCKET_ACCESS = "PUBLIC"
PRIVATE_BUCKET_ACCESS = "PRIVATE"
