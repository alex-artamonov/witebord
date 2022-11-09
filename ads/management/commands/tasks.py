from datetime import date, timedelta, datetime
from django.core.mail import send_mass_mail

import Witebord.settings as ws
from ads import models as am
from django.contrib.auth import get_user_model

DT_FORMAT = "%Y-%m-%d"
TODAY = date.today()
WEEK_AGO = TODAY + timedelta(-7)
URL_PART = "http://localhost:8000"


def my_job():
    #  Your job processing logic here...
    print(datetime.now())
    print(get_subscribers_list())
    # print(get_weekly_ads())
    message_body = f"Список объявлений за неделю: {get_weekly_ads()}"
    print(message_body)
    message = (
        f"{URL_PART}: еженедельная рассылка",
        message_body,
        ws.DEFAULT_FROM_EMAIL,
        get_subscribers_list(),
    )
    send_mass_mail((message,), fail_silently=False)


def get_subscribers_list():
    users = get_user_model()
    output = [user.email for user in users.objects.filter(is_subscribed=True)]
    return output


def get_weekly_ads():
    ads_list = [
        URL_PART + ad.get_absolute_url()
        for ad in am.Ad.objects.filter(created_at__lte=TODAY, created_at__gt=WEEK_AGO)
    ]
    if not ads_list:
        return f"К сожалению, на сайте {URL_PART} за прошедшую неделю новых объявлений не было."
    return ads_list
