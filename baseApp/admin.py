from django.contrib import admin
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from .models import Category, UserAdditionalDetails, StartUp, Product, Updates, UserIp, ProductRatingsAndReviews
=======
from .models import Category, UserAdditionalDetails, StartUp, Product, Updates, UserIp, ProductRatingsAndReviews, ProductTestimonials
>>>>>>> Stashed changes
=======
from .models import Category, UserAdditionalDetails, StartUp, Product, Updates, UserIp, ProductRatingsAndReviews, ProductTestimonials
>>>>>>> Stashed changes

admin.site.register(UserAdditionalDetails)
admin.site.register(Category)
admin.site.register(StartUp)
admin.site.register(Product)
admin.site.register(Updates)
admin.site.register(UserIp)
admin.site.register(ProductRatingsAndReviews)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
admin.site.register(ProductTestimonials)
>>>>>>> Stashed changes
=======
admin.site.register(ProductTestimonials)
>>>>>>> Stashed changes
