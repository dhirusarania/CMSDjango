from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserAdditionalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True, blank=True)
    fb_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    insta_link = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    house_no = models.IntegerField(null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    display_pic = models.ImageField(upload_to='user_images', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    last_login_ip = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserAdditionalDetails.objects.create(user=instance)


class UserIp(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_ip = models.CharField(max_length=50, blank=True, null=True)
    login_date_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Username - ' + str(self.user) + ', IP Address - ' + str(self.user_ip) + ', Login Date Time - ' + str(self.login_date_time)


class Category(models.Model):
    category = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='category_added_by')
    added_date = models.DateField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.category


class StartUp(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='startup_added_by')
    added_date = models.DateField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    deleted_flag = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)
    key_team_members = models.CharField(max_length=200, blank=True, null=True)
    incubators = models.CharField(max_length=500, blank=True, null=True)
    accelerators = models.CharField(max_length=500, blank=True, null=True)
    investors = models.CharField(max_length=500, blank=True, null=True)
    date_of_launch = models.DateField()
    name_of_founders = models.CharField(max_length=500, blank=True, null=True)
    year_founded = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, default='State')
    country = models.CharField(max_length=50)
    partnerships_associations = models.CharField(max_length=500, blank=True, null=True)
    funding_round = models.IntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='startup_images', blank=True, null=True)
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    pitch = models.TextField(default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='product_added_by')
    added_date = models.DateField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    deleted_flag = models.BooleanField(default=False)
    startup_name = models.ForeignKey(StartUp, related_name='startup_products', on_delete=models.PROTECT)
    stage = models.IntegerField()
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    product_app_link = models.CharField(max_length=200)
    active_users = models.IntegerField()
    product_video = models.FileField(upload_to='product_videos/', blank=True, null=True)

    def __str__(self):
        return self.product_name


class Updates(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    latest_updates = models.TextField()
    update_video = models.FileField(upload_to='product_videos/', blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='update_added_by')
    added_date = models.DateField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)


class ProductRatingsAndReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    reviews = models.TextField(blank=True, null=True)
    added_date = models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.product) + " - " + str(self.user)


<<<<<<< Updated upstream
<<<<<<< Updated upstream
class Pitch_Campaign(models.Model):
    startup = models.ForeignKey(StartUp, on_delete=models.CASCADE)
    ppt_upload = models.FileField(upload_to='ppt_upload/', blank=True, null=True)
    image_or_video_upload = models.FileField(upload_to='pitch_video_upload/', blank=True, null=True)

    def __str__(self):
        return str(self.startup)
=======
=======
>>>>>>> Stashed changes
class ProductTestimonials(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    userName = models.CharField(max_length=50)
    userImage = models.ImageField(upload_to='testimonial_images/')
    testimonial = models.TextField()

    def __str__(self):
        return str(self.product)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
