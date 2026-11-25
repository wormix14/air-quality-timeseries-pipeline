from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_pipeline
from datetime import datetime

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, trigger="interval", minutes=10, max_instances=1,next_run_time=datetime.now())
    scheduler.start()