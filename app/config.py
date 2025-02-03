from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

@dataclass
class Config(Singleton):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_FILE: Path = BASE_DIR / "logfile.log"
    MOOVIES_CHAT_USERNAME: str = "@xffilmsx"
    OWNER_USERNAME: str = "vladyslavcrane"
    CRON_SCHEDULE: Dict[str, Any] = None
    MOCK_DATA: bool = False

    def __post_init__(self):
        if self.CRON_SCHEDULE is None:
            self.CRON_SCHEDULE = {
                "POST_MOVIE": {
                    "trigger": "cron",
                    "hour": 19,
                    "minute": 30,
                    "timezone": "Europe/Istanbul",
                }
            }

config = Config()
