from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from Witebord import settings
from .models import Reply


@receiver(post_save, sender=Reply)
def notify_followers(sender, instance, created, **kwargs):
    # if not created:
    # print('hi from notify_followers', kwargs)
    # print(f'{created =}')
    # print('hi from notify_followers', sender, instance)
    # print(f'{instance.get_absolute_url()=}')
    if created:
        ad = instance.parent_ad
        link = "http://localhost:8000" + ad.get_absolute_url()
        # print('hi from Reply.created', link)
        body = f"На ваше объявление {link} пользователь {instance.author.username} оставил отклик"
        email_to = ad.author.email
        print(email_to)
        send_mail(
            message=body,
            subject="Новый отклик на объявление на сайте Witebord",
            from_email="sat.arepo@yandex.ru",
            recipient_list=[email_to],
            fail_silently=not settings.DEBUG,
        )


@receiver(post_save, sender=Reply)
def notify_accepted(sender, instance, created, **kwargs):
    d = {**kwargs}
    print(d)

    if instance.accepted:
        ad = instance.parent_ad
        link = "http://localhost:8000" + ad.get_absolute_url()
        print(instance.id, instance.content, instance.accepted)
        body = f"Ваш отклик '{instance.content}' на объявление {link} принят."
        email_to = instance.author.email
        print(email_to)
        send_mail(
            message=body,
            subject="Ваш отклик на объявление на сайте Witebord принят",
            from_email="sat.arepo@yandex.ru",
            recipient_list=[email_to],
            fail_silently=not settings.DEBUG,
        )
