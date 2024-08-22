from django.db import models
from django.conf import settings

class TelegramNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, sent, failed

    def __str__(self):
        return f"Notification for {self.user.username} at {self.sent_at}"
