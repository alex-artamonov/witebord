from django.db import models as m
from django.urls import reverse_lazy
# from django.contrib.auth import get_user_model
from django.conf import settings

# import users.models as um


# Create your models here.

# User = get_user_model()

class Guild(m.Model):
    name = m.CharField(max_length=25,
                       unique=True,
                       blank=False,
                       null=False,
                       verbose_name="Наименование")
    description = m.TextField(verbose_name="Описание")
    image = m.ImageField(
        upload_to='pics/guilds',
        null=True,
        blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('guild_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-name']
        verbose_name = "Гильдия"
        verbose_name_plural = 'Гильдии'


class Ad(m.Model):
    author = m.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=m.CASCADE,
        verbose_name="Автор",
        null=False,
        blank=False)
    title = m.CharField(
        verbose_name='Заголовок',
        max_length=100,
        null=False,
        blank=False)
    content = m.TextField(null=False,
                          blank=False)
    media_content = m.ImageField(upload_to="pics/%Y/%m/%d/", null=True, blank=True)
    created_at = m.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")
    updated_at = m.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования")

    def __str__(self) -> str:
        return f"{self.title=}"

    def preview(self):
        return self.content[:124] + '...'

    def get_absolute_url(self):
        return reverse_lazy('ad_detail', kwargs={'ad_id': self.id})

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = 'Объявления'


# class Reply(m.Model):
#     pass


class Tag(m.Model):
    name = m.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Метка",
        unique=True,
    )
    ads = m.ManyToManyField(
        to=Ad,
        db_constraint=True,
        db_table='ads_tags',
)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Метка"
        verbose_name_plural = 'Метки'


# class AdsTags(m.Model):
#     ad = m.ForeignKey(Ad, on_delete=m.CASCADE)
#     tag = m.ForeignKey(Tag, on_delete=m.CASCADE)
#
#     class Meta:
#         constraints = [
#             m.UniqueConstraint('ad_id', 'tag_id', name='unique_ad_tag')
#         ]
