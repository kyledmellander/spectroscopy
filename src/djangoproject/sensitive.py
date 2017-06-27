EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'testing@example.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spectrodb',

        #These settings are specific to postgresql
        'USER':'myprojectuser',
        'PASSWORD':'password',
        'HOST':'localhost',
        'PORT':'',
    }
}