from threading import Event, Thread
from schedule import every, run_pending
from time import sleep
from db import set_cpfh, get_users_id


def set_all_daily_calories():
    for user_id in get_users_id():
        set_cpfh(*user_id)
        print("in set_all_daily_calories", *user_id)
        sleep(0.001)


def schedule_set_calories():
    cease_continuous_run = Event()

    class ScheduleThread(Thread):
        def run(self):
            while not cease_continuous_run.is_set():
                run_pending()
                sleep(1)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

every().day.at("23:09").do(set_all_daily_calories)

