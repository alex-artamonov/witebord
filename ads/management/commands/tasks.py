from ads import models as am
from django.contrib.auth import get_user_model
# from users import models as um



def my_job():
    #  Your job processing logic here...
    print(get_subscribers_list())


def get_subscribers_list():
    users = get_user_model()
    output = [user.email for user in users.objects.filter(is_subscribed=True)]
    return output
