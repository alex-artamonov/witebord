import random

from users.models import User

MY_FILE = './utils/slovo'
NAMES_FILE = './utils/male_names'

def get_random_paragraph():
    with open(MY_FILE) as reader:
        slovo = reader.read().split('\n')   

    clean_result = [item for item in slovo if item] #getting rid of empty strings
    
    return random.sample(clean_result, k=1)[0]


def get_email(first_name, last_name):
    # with open(NAMES_FILE) as reader:
    #     names = reader.read().split('\n')
    
    domains = ['apple.ru', 'lemon.by', 'orange.com', 'pear.biz', 'cabbage.com' ]

    result = f"{first_name}.{last_name}@{random.choice(domains)}"
    return result


def create_random_users(number=1):
    with open(NAMES_FILE) as reader:
            names = reader.read().split('\n')

    usrs = []
    for i in range(number):
        first_name = random.choice(names)
        last_name = random.choice(names)
        username = first_name[0].lower()+last_name.lower()
        email = get_email(first_name, last_name)  
        print(first_name, last_name)
        usr = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username = username,
            email=email.lower(),
        )
        usrs.append(usr)

    print(usrs)