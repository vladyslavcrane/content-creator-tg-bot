from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"

MOOVIES_CHAT_USERNAME = "@xffilmsx"
OWNER_USERNAME = "@vladyslavcrane"

CRON_SCHEDULE = {
    "POST_MOVIE": {
        "trigger": "cron",
        # "start_date": datetime.now(),
        "hour": 19,
        "minute": 30,
        "timezone": "Europe/Istanbul",
    }
}
