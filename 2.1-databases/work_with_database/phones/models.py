from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название модели")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to="", verbose_name="Изображение")
    release_date = models.DateField(verbose_name="Дата релиза")
    lte_exists = models.BooleanField(default=False, verbose_name="Наличие LTE")
    slug = models.SlugField(blank=True, unique=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs) 