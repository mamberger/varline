from django.db import models


class APK(models.Model):
    apk_file = models.FileField(upload_to='apk/')
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return f'apk {self.id}'

    class Meta:
        verbose_name = 'apk'
        verbose_name_plural = 'apk'
