Rememeber to add these settings to your settings.py

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'accounts.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
}


# DEFAULT USER MODEL
AUTH_USER_MODEL = 'accounts.User'

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://127.0.0.1:5173,http://localhost:5173', cast=Csv())


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# DEFAULT USER MODEL
AUTH_USER_MODEL = 'accounts.User'



In your installed_apps, add:

# Third-Party Apps
'rest_framework',
'rest_framework_simplejwt.token_blacklist',
'corsheaders',