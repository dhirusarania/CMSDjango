from django.db import models


class HomeCMS(models.Model):
    title = models.CharField(max_length=100)
    header_img = models.ImageField(
        upload_to='home_images', blank=True, null=True)
    header_text_1 = models.CharField(max_length=500, blank=True, null=True)
    header_text_2 = models.CharField(max_length=500, blank=True, null=True)
    header_text_3 = models.CharField(max_length=500, blank=True, null=True)
    site_color = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to='home_images', blank=True, null=True)
    active = models.BooleanField(default=False)
    website_name = models.CharField(max_length=500, blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class CategoryCMS(models.Model):
    title = models.CharField(max_length=100)
    background_image = models.ImageField(
        upload_to='category_images', blank=True, null=True)
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
    about_image = models.ImageField(
        upload_to='about_images', blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class FooterCMS(models.Model):
    title = models.CharField(max_length=100)
    about_us = models.TextField()
    facebook = models.URLField(max_length=250, null=True, blank=True)
    twitter = models.URLField(max_length=250, null=True, blank=True)
    google = models.URLField(max_length=250, null=True, blank=True)
    pinterest = models.URLField(max_length=250, null=True, blank=True)
    youtube = models.URLField(max_length=250, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class ContactUsForm(models.Model):
    title = models.CharField(max_length=100)
    form = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class HomeComponents(models.Model):
    key = models.CharField(max_length=50)
    value = models.TextField()

    def __str__(self):
        return str(self.key)

class ContactModule(models.Model):
    value = models.TextField(default="{}")


    #timestamps
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.value)


class StaticComponents(models.Model):
    title = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    button = models.TextField(blank=True, null=True)
    bgcolor = models.TextField(blank=True, null=True)
    button_url = models.TextField(blank=True, null=True)
    bgimage = models.ImageField(
        upload_to='static_components', blank=True, null=True)

    def __str__(self):
        return str(self.name)
