import logging
import threading
import time

import schedule


logger = logging.getLogger(__name__)
scheduler_running = None


def setup_scheduler():
    global scheduler_running

    def run_continuously():
        while scheduler_running:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run_continuously)
    thread.daemon = True
    logger.info('~ starting continuous thread')
    scheduler_running = True
    thread.start()


def teardown_scheduler():
    global scheduler_running
    scheduler_running = False
