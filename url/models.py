import os
import base64

from django.db import models

from urlShortner.settings import SHORT_URL_LENGTH

class Url(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    original_url = models.CharField(max_length=2048)
    short_url = models.CharField(max_length=SHORT_URL_LENGTH, unique=True, default=None)
    active = models.BooleanField(default=True)
    use_counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = self.generate_random_code(SHORT_URL_LENGTH)
        super(Url, self).save(*args, **kwargs)

    @classmethod
    def generate_random_code(cls, str_len: int):
        return base64.b64encode(os.urandom(str_len), altchars=b'aA').decode('ascii')[:str_len]
