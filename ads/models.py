from django.db import models as m
from django.urls import reverse_lazy

from django.conf import settings


class Guild(m.Model):
    """пользователь обязательно должен определить объявление в одну из следующих
    - категорий:
    -- Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний."""

    name = m.CharField(
        max_length=25, unique=True, blank=False, null=False, verbose_name="Наименование"
    )
    description = m.TextField(verbose_name="Описание")
    image = m.ImageField(upload_to="pics/guilds", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("ads:guild_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-name"]
        verbose_name = "Гильдия"
        verbose_name_plural = "Гильдии"


class Ad(m.Model):
    """Объявления состоят из
    -- заголовка и
    -- текста, внутри которого могут быть
    -- картинки, встроенные видео и другой контент."""

    author = m.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=m.CASCADE,
        verbose_name="Автор",
        null=False,
        blank=False,
    )
    title = m.CharField(
        verbose_name="Заголовок", max_length=100, null=False, blank=False
    )
    content = m.TextField(verbose_name="Содержание", null=False, blank=False)
    media_content = m.ImageField(
        verbose_name="Изображение/Видео",
        upload_to="pics/%Y/%m/%d/",
        null=True,
        blank=True,
    )
    created_at = m.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = m.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    guild = m.ForeignKey(
        verbose_name="Гильдия",
        to=Guild,
        on_delete=m.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.title=}"

    def preview(self):
        return self.content[:124] + "..."

    def get_absolute_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Tag(m.Model):
    """Метки для поиска. В ТЗ не было"""

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
        db_table="ads_tags",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Метка"
        verbose_name_plural = "Метки"


class Reply(m.Model):
    """Пользователи могут отправлять отклики на объявления других пользователей,
    состоящие из простого текста."""

    author = m.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=m.CASCADE,
        verbose_name="Автор",
        null=False,
        blank=False,
    )
    content = m.TextField(null=False, blank=False, verbose_name="Текст")
    parent_ad = m.ForeignKey(to=Ad, null=False, blank=False, on_delete=m.CASCADE)
    created_at = m.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = m.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    accepted = m.BooleanField(null=True, verbose_name="Принят")

    def __str__(self) -> str:
        return self.content

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
