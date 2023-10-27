from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(null=True , blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class ShortTermCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='short_term_courses')
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    amount = models.FloatField()
    description = models.TextField(max_length = 2000)
    image = models.ImageField(null=True , blank=True)
    status = models.BooleanField(default=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    