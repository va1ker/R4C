from .settings import * #noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "tests.sqlite3"), #noqa: F405
    }
}
