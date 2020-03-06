from django.contrib import admin
from .models import HomeCMS, CategoryCMS, ContactCMS, AboutCMS, FooterCMS, ContactUsForm, HomeComponents, StaticComponents

admin.site.register(HomeCMS)
admin.site.register(CategoryCMS)
admin.site.register(ContactCMS)
admin.site.register(AboutCMS)
admin.site.register(FooterCMS)
admin.site.register(ContactUsForm)
admin.site.register(HomeComponents)
admin.site.register(StaticComponents)
