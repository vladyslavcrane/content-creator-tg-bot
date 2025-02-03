from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config


def setup_scheduler(bot, jobs):
    scheduler = AsyncIOScheduler()

    job_kwargs = {
        "bot": bot,
        "chat_id": config.MOOVIES_CHAT_USERNAME,
    }

    for job, params in jobs:
        scheduler.add_job(job, **params, kwargs=job_kwargs)

    scheduler.start()
