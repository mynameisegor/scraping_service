from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города')
    slug = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия городов'

    def __str__(self):
        return self.name
