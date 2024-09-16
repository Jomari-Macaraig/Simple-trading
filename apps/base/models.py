from django.db import models

DECIMAL_MAX_DIGITS = 32
DECIMAL_MAX_DECIMAL_PLACES = 8


class Audit(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
