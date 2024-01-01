from schedule import repeat, every, run_pending
from db import set_daily_calories, get_users_id

@repeat(every().day.at("00:00"))
def set_all_daily_calories():
    for user_id in get_users_id():
        set_daily_calories(user_id)


def schedule_set_calories():
    while True:
        run_pending()
