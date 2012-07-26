from django.db import models
from django.db.models import Q

class EnqueuedMessage(models.Model):
    sent_at = models.DateField(auto_now=True, db_index=True)
    message = models.TextField()
    recipient = models.CharField(db_index=True, max_length=255) # not using contacts so we can query the field

    @classmethod
    def messages_for(cls, country_code):
        messages = EnqueuedMessage.objects.filter(Q(recipient__startswith=country_code)|Q(sent_at__lt=(datetime.datetime.now() - datetime.timedelta(seconds=self.max_delay))))
        return messages
