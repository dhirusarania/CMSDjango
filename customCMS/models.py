from django.db import models


class HomeCMS(models.Model):
    title = models.CharField(max_length=100)
    header_img = models.ImageField(upload_to='home_images', blank=True, null=True)
    header_text_1 = models.CharField(max_length=500, blank=True, null=True)
    header_text_2 = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class CategoryCMS(models.Model):
    title = models.CharField(max_length=100)
    background_image = models.ImageField(upload_to='category_images', blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class ContactCMS(models.Model):
    title = models.CharField(max_length=100)
    contact_info = models.TextField()
    location = models.CharField(max_length=200)
    phone1 = models.BigIntegerField()
    phone2 = models.BigIntegerField()
    email = models.EmailField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class AboutCMS(models.Model):
    title = models.CharField(max_length=100)
    about_info = models.TextField()
    about_image = models.ImageField(upload_to='about_images', blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class FooterCMS(models.Model):
    title = models.CharField(max_length=100)
    about_us = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class ContactUsForm(models.Model):
    title = models.CharField(max_length=100)
    form = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.title)
