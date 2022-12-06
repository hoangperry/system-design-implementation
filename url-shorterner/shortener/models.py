from django.db import models


class Shorten(models.Model):
    id = models.BigIntegerField(primary_key=True)
    shorten = models.CharField(max_length=7)
    origin = models.CharField(max_length=512)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'shortener'
