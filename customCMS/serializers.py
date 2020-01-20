from rest_framework import serializers
from .models import HomeCMS, CategoryCMS, ContactCMS, AboutCMS, FooterCMS, ContactUsForm
from baseApp.models import Category


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeCMS
        fields = '__all__'


class CategoryCMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryCMS
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactCMS
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutCMS
        fields = '__all__'


class CategoryStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['deleted_flag']


class FooterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FooterCMS
        fields = '__all__'


class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUsForm
        fields = '__all__'
