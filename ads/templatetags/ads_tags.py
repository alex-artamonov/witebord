from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count

from ..models import Guild


User = get_user_model()


register = template.Library()


@register.simple_tag
def get_guilds_list():
    return Guild.objects.annotate(cnt=Count('user'))


@register.simple_tag
def get_users_list():
    return User.objects.annotate(cnt=Count('ad'))
