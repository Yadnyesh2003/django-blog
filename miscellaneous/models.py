from django.db import models

# Create your models here.

class About(models.Model):
    about_heading = models.CharField(max_length=50)
    about_description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "about"

    def __str__(self):
        return self.about_heading

class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "social links"

    def __str__(self):
        return self.platform

