from django.db import models

# Create your models here.


class Courts(models.Model):
    court_name = models.TextField()
    scrape_type = models.IntegerField()


class Total(models.Model):
    till_date = models.DateField()
    scrape_type = models.IntegerField()
    orders = models.IntegerField()
    judgements = models.IntegerField()
