from django.db import models


class Matzip(models.Model):
    post_url = models.CharField(max_length=200, default=None)
    img_url = models.CharField(max_length=4000, default=None)
    keyword = models.CharField(max_length=30)
    allowed = models.BooleanField()

    def __str__(self):
        return self.keyword
