from rest_framework import serializers
from .models import Category, UserAdditionalDetails, StartUp, Product, Updates, ProductRatingsAndReviews, ProductTestimonials
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')


class UserAdditionalDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAdditionalDetails
        fields = '__all__'


class UserLogOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAdditionalDetails
        fields = ['login_status']


class StartupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartUp
        fields = '__all__'



class StartupFeaturedSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartUp
        fields = [
            'featured'
        ]


class PasswordChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password', 'pk']

        read_only_fields = ('pk', )


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

        depth = 2


class ProductSerializerWD(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class DeleteProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['deleted_flag']


class DeleteStartupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartUp
        fields = ['deleted_flag']


class StartupSerializerWithDepth(serializers.ModelSerializer):

    class Meta:
        model = StartUp
        fields = '__all__'

        depth = 1


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Updates
        fields = '__all__'


class UpdateSerializerWD(serializers.ModelSerializer):

    class Meta:
        model = Updates
        fields = '__all__'

        depth = 1


class DeleteUpdateSerializerWD(serializers.ModelSerializer):

    class Meta:
        model = Updates
        fields = ['deleted_flag']


class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


class StartupSerializerWithProducts(serializers.ModelSerializer):
    startup_products = ProductSerializerWD(many=True, read_only=True)

    class Meta:
        model = StartUp
        fields = ['id', 'name', 'year_founded', 'city', 'state', 'country', 'startup_products']



class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRatingsAndReviews
        fields = '__all__'



class RatingsSerializerWD(serializers.ModelSerializer):

    class Meta:
        model = ProductRatingsAndReviews
        fields = '__all__'

        depth = 1


class ProductTestimonialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTestimonials
        fields = '__all__'
