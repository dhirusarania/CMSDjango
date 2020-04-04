from django.contrib import admin
from .models import Category, UserAdditionalDetails, StartUp, Product, Updates, UserIp, ProductRatingsAndReviews, ProductTestimonials

admin.site.register(UserAdditionalDetails)
admin.site.register(Category)
admin.site.register(StartUp)
admin.site.register(Product)
admin.site.register(Updates)
admin.site.register(UserIp)
admin.site.register(ProductRatingsAndReviews)
admin.site.register(ProductTestimonials)
