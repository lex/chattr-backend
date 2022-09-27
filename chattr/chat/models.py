from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Message(models.Model):
    username = models.CharField(max_length=64, editable=False)
    message = models.CharField(max_length=1024, editable=False)
    channel = models.ForeignKey(
        Channel, related_name='messages', on_delete=models.CASCADE, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{} - {}: {}'.format(self.channel, self.username, self.message)

    class Meta:
        ordering = ('timestamp',)
