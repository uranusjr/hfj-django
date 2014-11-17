from django.db import models


class BlogEntry(models.Model):
    class Meta:
        verbose_name = 'Blog entry'
        verbose_name_plural = 'Blog entries'

    def __unicode__(self):
        pass
