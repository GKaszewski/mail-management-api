from django.db import models

class MailProvider(models.Model):
    host = models.URLField()
    port = models.IntegerField(default=587)
    host_user = models.CharField(max_length=255)
    host_password = models.CharField(max_length=255)
    use_tls = models.BooleanField(default=True)
    from_email = models.EmailField()

    def __str__(self):
        return f"{self.host} ({self.from_email})"