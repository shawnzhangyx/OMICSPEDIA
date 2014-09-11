import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
if len(DATABASES['default']) ==0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'omicspedia',
            'USER': 'omics_admin',
            'PASSWORD':'123456',
            'HOST': 'localhost',
            'PORT': 5432,
            }
    }