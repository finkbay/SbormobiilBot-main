from django.db import models


class Profile(models.Model):
    name = models.TextField(
        verbose_name='Название материала'
    )
    amount = models.TextField(
        verbose_name='кол-во собранного материала'
    )

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Timetable(models.Model):
    date = models.DateTimeField(
        verbose_name='Дата-время'
    )
    street = models.TextField(
        verbose_name='Место сбора'
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'


class UserReport(models.Model):
    user_id = models.TextField(
        verbose_name='ID пользователя'
    )

    material = models.TextField(
        verbose_name='Название материала'
    )
    amount = models.TextField(
        verbose_name='кол-во собранного материала'
    )

    class Meta:
        verbose_name = 'Отчёты пользователей'
        verbose_name_plural = 'Отчёты пользователей '
