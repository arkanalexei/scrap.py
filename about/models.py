from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.conf import settings

class Feedback(models.Model):
    name = models.CharField(max_length=1000, default="")
    message = models.CharField(max_length=2000, default ="")
    star = models.CharField(max_length=1000, choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], default='5')
    created_at = models.DateTimeField(auto_now_add=True,null=True) 
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)