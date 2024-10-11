from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Guild


User = get_user_model()


register = template.Library()


@register.simple_tag
def get_guilds_list():
    return Guild.objects.annotate(cnt=Count("user"))


@register.simple_tag
def get_users_list():
    return User.objects.all()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
