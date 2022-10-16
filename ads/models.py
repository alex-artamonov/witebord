from django.db import models as m
from django.urls import reverse_lazy

import users.models as um


# Create your models here.

class Guild(m.Model):
    name = m.CharField(max_length=25,
                       unique=True,
                       blank=False,
                       null=False,
                       verbose_name="Наименование")
    description = m.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = "Гильдия"
        verbose_name_plural = 'Гильдии'


class Ad(m.Model):
    author = m.ForeignKey(
        to=um.User,
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
        return reverse_lazy('ad_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = 'Объявления'
