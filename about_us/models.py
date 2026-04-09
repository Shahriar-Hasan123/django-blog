from django.db import models

# Create your models here.


class About(models.Model):
    about_heading = models.CharField(max_length=30)
    about_description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.about_heading


class SocialLink(models.Model):
    platform = models.CharField(max_length=30)
    link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.platform
