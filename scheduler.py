from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import MOOVIES_CHAT_USERNAME


def setup_scheduler(bot, jobs):
    scheduler = AsyncIOScheduler()
    
    job_kwargs = {
        "bot": bot,
        "user_id": MOOVIES_CHAT_USERNAME,
    }

    for job, params in jobs:
        scheduler.add_job(job, **params, kwargs=job_kwargs)

    scheduler.start()
