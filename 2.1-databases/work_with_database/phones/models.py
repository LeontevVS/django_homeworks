from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    price = models.FloatField(null=False)
    image = models.CharField(max_length=100, null=False)
    release_date = models.DateField(null=False)
    lte_exists = models.BooleanField(null=False)
    slug = models.SlugField(max_length=100, null=False, unique=True)

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(**kwargs)