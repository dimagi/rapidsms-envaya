from django.db import models
from django.db.models import Q
import datetime

class EnqueuedMessage(models.Model):
    sent_at = models.DateField(auto_now=True, db_index=True)
    message = models.TextField()
    recipient = models.CharField(db_index=True, max_length=255) # not using contacts so we can query the field

    @classmethod
    def messages_for(cls, country_code, max_delay):
        if max_delay is not None:
            messages = cls.objects.filter(Q(recipient__startswith=country_code)|Q(sent_at__lt=(datetime.datetime.now() - datetime.timedelta(seconds=max_delay))))
        else:
            messages = cls.objects.filter(recipient__startswith=country_code)
        return messages
