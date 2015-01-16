
DEBUG = True

COMPRESS_ENABLED = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "03a12404-490c-470a-af1c-b5dad3e6k18356a-b7fe-411b-b880-a7b5c04e23f2790587b7-8984-48a9-poop-a3f9b6b3b8a1"
NEVERCACHE_KEY = "2a434-39-80ae-40de-89fe7fb4f5696c7e-c347-4ea5-9664-6c7419c56c883dfe0347-ec7e-4b67-poop-58b23eae0519"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

SSLIFY_DISABLE = True

SITE_URL = 'localhost'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'planda.bot@gmail.com'
EMAIL_HOST_PASSWORD = 'littleangryactsnake'
EMAIL_PORT = 587
SERVER_EMAIL = "planda.bot@gmail.com"