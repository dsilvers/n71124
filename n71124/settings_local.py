# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')-ovlk99mme6agtq1=&*dkh$jk!u=5#@&q^r-$h7fsp0+(gyae'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}