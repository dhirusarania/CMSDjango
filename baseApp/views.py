from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Category, UserAdditionalDetails, StartUp, Product, UserIp, Updates, ProductRatingsAndReviews, ProductTestimonials
from .serializers import CategorySerializer, UserSerializer, UserAdditionalDetailsSerializer, StartupSerializer, \
    PasswordChangeSerializer, ProductSerializer, ProductSerializerWD, DeleteStartupSerializer, \
    UserLogOutSerializer, DeleteProductSerializer, StartupSerializerWithDepth, StartupFeaturedSerializer, UpdateSerializer, UpdateSerializerWD, \
    DeleteUpdateSerializerWD, SocialAuthSerializer, StartupSerializerWithProducts, RatingsSerializer, RatingsSerializerWD, ProductTestimonialsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import os
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions, status
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from social_core.backends.oauth import BaseOAuth2
from requests.exceptions import HTTPError
from rest_framework import filters
from django.db.models import Count

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_signin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_obj = User.objects.get(email=email)
    username = user_obj.username
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        ip_obj = UserIp()
        ip_obj.user = user
        ip_obj.user_ip = get_client_ip(request)
        ip_obj.save()
        user_obj = UserAdditionalDetails.objects.get(user=user)
        user_obj.login_status = True
        user_obj.last_login_ip = get_client_ip(request)
        user_obj.save()
        users_obj = User.objects.get(username=user)
        users_obj.last_login = datetime.now()
        users_obj.save()
        return Response({'token': token.key, 'id': user.id, 'username': user.username},
                        status=HTTP_200_OK)

    else:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    if username is None or password is None or email is None:
        return Response({'error': 'Please provide all credentials'},
                        status=HTTP_400_BAD_REQUEST)
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    user.save()
    Token.objects.get_or_create(user=user)
    return Response({'id': user.id, 'username': user.username},
                    status=HTTP_200_OK)


@permission_classes((AllowAny,))
class UserCount(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((AllowAny,))
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.filter(deleted_flag=False)
    serializer_class = CategorySerializer


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        User = UserSerializer(user)
        return Response(User.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAdditionalDetailsView(APIView):
    def get_object(self, pk):
        try:
            return UserAdditionalDetails.objects.get(user=pk)
        except UserAdditionalDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        User = UserAdditionalDetailsSerializer(user, context={"request": request})
        return Response(User.data)

    def put(self, request, pk):
        user_ext = self.get_object(pk)
        serializer = UserAdditionalDetailsSerializer(user_ext, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogOut(APIView):
    def get_object(self, pk):
        try:
            return UserAdditionalDetails.objects.get(user=pk)
        except UserAdditionalDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        User = UserLogOutSerializer(user, context={"request": request})
        return Response(User.data)

    def put(self, request, pk):
        user_ext = self.get_object(pk)
        serializer = UserLogOutSerializer(user_ext, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UserExtensionPostView(viewsets.ViewSet):
    def user_extension_list(self, request):
        queryset = UserAdditionalDetails.objects.all()
        serializer = UserAdditionalDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserAdditionalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartupListing(APIView):
    def get_object(self, pk):
        try:
            obj = StartUp.objects.filter(added_by=pk).filter(deleted_flag=False)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializer(startup, many=True, context={"request": request})
        return Response(StartUp.data)

    # def put(self, request, pk):
    #     startupobj = self.get_object(pk)
    #     serializer = StartupSerializer(startupobj, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartupPost(viewsets.ViewSet):
    def startup_list(self, request):
        queryset = StartUp.objects.all()
        serializer = StartupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StartupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartupById(APIView):
    def get_object(self, pk):
        try:
            return StartUp.objects.get(id=pk)
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializer(startup, context={"request": request})
        return Response(StartUp.data)

    def put(self, request, pk):
        startupobj = self.get_object(pk)
        serializer = StartupSerializer(startupobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     startupobj = self.get_object(pk)
    #     startupobj.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteStartup(APIView):
    def get_object(self, pk):
        try:
            return StartUp.objects.get(id=pk)
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = DeleteStartupSerializer(startup, context={"request": request})
        return Response(StartUp.data)

    def put(self, request, pk):
        startupobj = self.get_object(pk)
        serializer = DeleteStartupSerializer(startupobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    serializer_class = PasswordChangeSerializer
    queryset = User.objects.all()

    def put(self, request, format=None):
        response_data = {}
        id = request.data.get('id')
        password = request.data.get('password')
        user = User.objects.get(id=id)
        user.set_password(password)
        user.save()
        response_data['message'] = 'Password Changed Successfully'
        response_data['status'] = 200
        return Response(response_data, status=status.HTTP_200_OK)


def handle_uploaded_file(f):
    if not os.path.isdir("media/product_images/"):
        os.makedirs("media/product_images/")

    with open('media/product_images/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    return f.name


@permission_classes((AllowAny,))
class ProductUploadImage(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        print(self.request.FILES)

    def post(self, request, format=None):
        res = {}

        for i in self.request.FILES:
            array = {}
            array['success'] = 1
            res['url'] = 'http://103.228.113.9/media/product_images/' + handle_uploaded_file(self.request.FILES[i])
            array['file'] = res
        return Response(array)


class ProductPost(viewsets.ViewSet):
    def product_list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializerWD(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializerWD(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductByStartup(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.filter(startup_name=pk).filter(deleted_flag=False)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = ProductSerializer(product, context={"request": request}, many=True)
        return Response(Product.data)

    # def put(self, request, pk):
    #     startupobj = self.get_object(pk)
    #     serializer = StartupSerializer(startupobj, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     startupobj = self.get_object(pk)
    #     startupobj.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny,))
class ProductById(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = ProductSerializer(product, context={"request": request})
        return Response(Product.data)


class EditProduct(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = ProductSerializerWD(product, context={"request": request})
        return Response(Product.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ProductSerializerWD(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = DeleteProductSerializer(product, context={"request": request})
        return Response(Product.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = DeleteProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class AllStartupListing(APIView):
    def get_object(self):
        try:
            obj = StartUp.objects.filter(deleted_flag=False)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request):
        startup = self.get_object()
        StartUp = StartupSerializerWithDepth(startup, many=True, context={"request": request})
        return Response(StartUp.data)


@permission_classes((AllowAny,))
class StartUpByCategory(APIView):
    def get_object(self, pk):
        try:
            obj = StartUp.objects.filter(deleted_flag=False).filter(category=pk)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializer(startup, many=True, context={"request": request})
        return Response(StartUp.data)


@permission_classes((AllowAny,))
class StartupByIdWithDepth(APIView):
    def get_object(self, pk):
        try:
            return StartUp.objects.get(id=pk)
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializerWithDepth(startup, context={"request": request})
        return Response(StartUp.data)


@permission_classes((AllowAny,))
class ProductByStartupNoAuth(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.filter(startup_name=pk).filter(deleted_flag=False)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = ProductSerializer(product, context={"request": request}, many=True)
        return Response(Product.data)


@permission_classes((AllowAny,))
class CategoryById(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cat = self.get_object(pk)
        Cat = CategorySerializer(cat, context={"request": request})
        return Response(Cat.data)


class UpdatePost(viewsets.ViewSet):
    def update_list(self, request):
        queryset = Updates.objects.all()
        serializer = UpdateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UpdatesByProduct(APIView):
    def get_object(self, pk):
        try:
            obj = Updates.objects.filter(product=pk).filter(deleted_flag=False).order_by('-pk')
            return obj
        except Updates.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        Update = UpdateSerializer(update, many=True, context={"request": request})
        return Response(Update.data)


@permission_classes((AllowAny,))
class UpdateById(APIView):
    def get_object(self, pk):
        try:
            return Updates.objects.get(id=pk)
        except Updates.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        Update = UpdateSerializerWD(update, context={"request": request})
        return Response(Update.data)


class DeleteProductUpdate(APIView):
    def get_object(self, pk):
        try:
            return Updates.objects.get(id=pk)
        except Updates.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        Update = DeleteUpdateSerializerWD(update, context={"request": request})
        return Response(Update.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = DeleteUpdateSerializerWD(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProductUpdate(APIView):
    def get_object(self, pk):
        try:
            return Updates.objects.get(id=pk)
        except Updates.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        Update = UpdateSerializer(update, context={"request": request})
        return Response(Update.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = UpdateSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)

        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # generate JWT token
            login(request, authenticated_user)
            data = {
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            # customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token'),
                "id": authenticated_user.id
            }
            return Response(status=status.HTTP_200_OK, data=response)


@permission_classes((AllowAny,))
class UserCount(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((AllowAny,))
class FeaturedStartupListing(APIView):
    def get_object(self):
        try:
            obn = StartUp.objects.filter(deleted_flag=False)
            obj = obn.filter(featured=True)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request):
        startup = self.get_object()
        StartUp = StartupSerializerWithDepth(startup, many=True, context={"request": request})
        return Response(StartUp.data)


class StartupListingWithProducts(APIView):
    def get_object(self, pk):
        try:
            obj = StartUp.objects.filter(added_by=pk).filter(deleted_flag=False)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializerWithProducts(startup, many=True, context={"request": request})
        return Response(StartUp.data)


class RatingsPostView(viewsets.ViewSet):
    def ratings_list(self, request):
        queryset = ProductRatingsAndReviews.objects.all()
        serializer = RatingsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RatingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingsPutView(APIView):
    def get_object(self, pk):
        try:
            return ProductRatingsAndReviews.objects.get(user=pk)
        except ProductRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = RatingsSerializer(obj, context={"request": request})
        return Response(Obj.data)


class UserRatingsPutView(APIView):
    def get_object(self, pk):
        try:
            return ProductRatingsAndReviews.objects.get(id=pk)
        except ProductRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = RatingsSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = RatingsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UserProductReviews(generics.ListAPIView):
    queryset = ProductRatingsAndReviews.objects.all()
    serializer_class = RatingsSerializerWD


@permission_classes((AllowAny,))
class StartupSearch(generics.ListAPIView):
    queryset = StartUp.objects.all()
    serializer_class = StartupSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name', 'description']

    def get_queryset(self):
        qs = StartUp.objects.all()
        logging.debug(qs.query)
        return qs





@permission_classes((AllowAny,))
class FeaturedStartupListing(APIView):
    def get_object(self):
        try:
            obn = StartUp.objects.filter(deleted_flag=False)
            obj = obn.filter(featured=True)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request):
        startup = self.get_object()
        StartUp = StartupSerializerWithDepth(startup, many=True, context={"request": request})
        return Response(StartUp.data)


class StartupListingWithProducts(APIView):
    def get_object(self, pk):
        try:
            obj = StartUp.objects.filter(added_by=pk).filter(deleted_flag=False)
            return obj
        except StartUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        startup = self.get_object(pk)
        StartUp = StartupSerializerWithProducts(startup, many=True, context={"request": request})
        return Response(StartUp.data)


class RatingsPostView(viewsets.ViewSet):
    def ratings_list(self, request):
        queryset = ProductRatingsAndReviews.objects.all()
        serializer = RatingsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RatingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingsPutView(APIView):
    def get_object(self, pk):
        try:
            return ProductRatingsAndReviews.objects.get(user=pk)
        except ProductRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = RatingsSerializer(obj, context={"request": request})
        return Response(Obj.data)


class UserRatingsPutView(APIView):
    def get_object(self, pk):
        try:
            return ProductRatingsAndReviews.objects.get(id=pk)
        except ProductRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = RatingsSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = RatingsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UserProductReviews(generics.ListAPIView):
    queryset = ProductRatingsAndReviews.objects.all()
    serializer_class = RatingsSerializerWD

import django_filters.rest_framework

@permission_classes((AllowAny,))
class StartupSearch(generics.ListAPIView):
    queryset = StartUp.objects.all()
    serializer_class = StartupSerializer
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['$name', 'description']
    filterset_fields = ['category']

    

    def get_queryset(self):
         qs = StartUp.objects.all()
         print(qs.query)
         return qs


class TestimonialPost(viewsets.ViewSet):
    def testimonial_list(self, request):
        queryset = ProductTestimonials.objects.all()
        serializer = ProductTestimonialsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductTestimonialsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ProductTestimonialsList(APIView):
    def get_object(self, pk):
        try:
            obj = ProductTestimonials.objects.filter(product=pk)
            return obj
        except ProductTestimonials.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = ProductTestimonialsSerializer(obj, many=True, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class MakeFeatured(generics.RetrieveUpdateAPIView):
    queryset = StartUp.objects.all()
    serializer_class = StartupFeaturedSerializer
    lookup_fields = "id"



from customCMS.models import CategoryCMS   

@permission_classes((AllowAny,))
class getAboutMetrics(APIView):
    def get(self, request, format=None):  
        response_data = {}

        listings = StartUp.objects.count()

        user_count = User.objects.filter(is_superuser = False, is_staff = False).count()

        user_count = User.objects.filter(is_superuser = False, is_staff = False).count()

        category = Category.objects.filter(deleted_flag = False).count()

        response_data['listing'] = listings
        response_data['users'] = user_count
        response_data['category'] = category
            

        


        return Response(response_data, status=status.HTTP_200_OK)




