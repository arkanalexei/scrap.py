from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class WasteDeposit(models.Model):
    CHOICES = (
            ("PLASTIK", "Plastik"),
            ("KACA", "Kaca / Beling"),
            ("KERTAS", "Kertas / Kardus"),
            ("ETC", "Organik & Lainnya")
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    mass = models.FloatField()
    description = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=32, choices=CHOICES, default=CHOICES[0])

