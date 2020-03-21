from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from django.http import Http404
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, viewsets
from .models import HomeCMS, CategoryCMS, ContactCMS, AboutCMS, FooterCMS, ContactUsForm, HomeComponents
from .serializers import HomeSerializer, CategoryCMSSerializer, ContactSerializer, AboutSerializer, \
    CategoryStatusSerializer, FooterSerializer, ContactFormSerializer, HomeComponentsSerializer
from baseApp.models import Category
from baseApp.serializers import CategorySerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user.is_superuser:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'username': user.username}, status=HTTP_200_OK)


# @permission_classes((AllowAny,))
class HomeCMSView(viewsets.ViewSet):
    def home_cms_list(self, request):
        queryset = HomeCMS.objects.all()
        serializer = HomeSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = HomeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ActvatedHomeCMSView(viewsets.ViewSet):
    def activated_list(self, request):
        queryset = HomeCMS.objects.filter(active=True)
        serializer = HomeSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class EditHomeCMS(APIView):
    def get_object(self, pk):
        try:
            return HomeCMS.objects.get(pk=pk)
        except HomeCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = HomeSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = HomeSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveHomeCMS(APIView):
    def get_object(self, pk):
        try:
            return HomeCMS.objects.get(pk=pk)
        except HomeCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = HomeSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = HomeCMS.objects.all()
        for i in obj:
            i.active = False
            i.save()
        obj = self.get_object(pk)
        obj.active = True
        obj.save()
        serializer = HomeSerializer(obj)
        return Response(serializer.data)


# @permission_classes((AllowAny,))
class CategoryCMSView(viewsets.ViewSet):
    def category_cms_list(self, request):
        queryset = CategoryCMS.objects.all()
        serializer = CategoryCMSSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryCMSSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCategoryCMS(APIView):
    def get_object(self, pk):
        try:
            return CategoryCMS.objects.get(pk=pk)
        except CategoryCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategoryCMSSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategoryCMSSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ActvatedCategoryCMSView(viewsets.ViewSet):
    def activated_list(self, request):
        queryset = CategoryCMS.objects.filter(active=True)
        serializer = CategoryCMSSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ActiveCategoryCMS(APIView):
    def get_object(self, pk):
        try:
            return CategoryCMS.objects.get(pk=pk)
        except CategoryCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategoryCMSSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = CategoryCMS.objects.all()
        for i in obj:
            i.active = False
            i.save()
        obj = self.get_object(pk)
        obj.active = True
        obj.save()
        serializer = CategoryCMSSerializer(obj)
        return Response(serializer.data)


class ContactCMSView(viewsets.ViewSet):
    def contact_cms_list(self, request):
        queryset = ContactCMS.objects.all()
        serializer = ContactSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditContactCMS(APIView):
    def get_object(self, pk):
        try:
            return ContactCMS.objects.get(pk=pk)
        except ContactCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = ContactSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ContactSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ActivatedContactCMSView(viewsets.ViewSet):
    def activated_list(self, request):
        queryset = ContactCMS.objects.filter(active=True)
        serializer = ContactSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ActiveContactCMS(APIView):
    def get_object(self, pk):
        try:
            return ContactCMS.objects.get(pk=pk)
        except ContactCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = ContactSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = ContactCMS.objects.all()
        for i in obj:
            i.active = False
            i.save()
        obj = self.get_object(pk)
        obj.active = True
        obj.save()
        serializer = ContactSerializer(obj)
        return Response(serializer.data)


class AboutCMSView(viewsets.ViewSet):
    def about_cms_list(self, request):
        queryset = AboutCMS.objects.all()
        serializer = AboutSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = AboutSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditAboutCMS(APIView):
    def get_object(self, pk):
        try:
            return AboutCMS.objects.get(pk=pk)
        except AboutCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = AboutSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = AboutSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ActivatedAboutCMSView(viewsets.ViewSet):
    def activated_list(self, request):
        queryset = AboutCMS.objects.filter(active=True)
        serializer = AboutSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ActiveAboutCMS(APIView):
    def get_object(self, pk):
        try:
            return AboutCMS.objects.get(pk=pk)
        except AboutCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = AboutSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = AboutCMS.objects.all()
        for i in obj:
            i.active = False
            i.save()
        obj = self.get_object(pk)
        obj.active = True
        obj.save()
        serializer = AboutSerializer(obj)
        return Response(serializer.data)


class CategoryView(viewsets.ViewSet):
    def category_cms_list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCategory(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategorySerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategorySerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryStatus(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategoryStatusSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategoryStatusSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FooterCMSView(viewsets.ViewSet):
    def footer_list(self, request):
        queryset = FooterCMS.objects.all()
        serializer = FooterSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = FooterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditFooterCMS(APIView):
    def get_object(self, pk):
        try:
            return FooterCMS.objects.get(pk=pk)
        except FooterCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = FooterSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = FooterSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ActivatedFooterCMSView(viewsets.ViewSet):
    def activated_list(self, request):
        queryset = FooterCMS.objects.filter(active=True)
        serializer = FooterSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ActiveFooterCMS(APIView):
    def get_object(self, pk):
        try:
            return FooterCMS.objects.get(pk=pk)
        except FooterCMS.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = FooterSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = FooterCMS.objects.all()
        for i in obj:
            i.active = False
            i.save()
        obj = self.get_object(pk)
        obj.active = True
        obj.save()
        serializer = FooterSerializer(obj)
        return Response(serializer.data)


class EditContactForm(APIView):
    def get_object(self, pk):
        try:
            return ContactUsForm.objects.get(pk=1)
        except ContactUsForm.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = ContactFormSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ContactFormSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class GetContactForm(APIView):
    def get_object(self, pk):
        try:
            return ContactUsForm.objects.get(pk=1)
        except ContactUsForm.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = ContactFormSerializer(obj, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class GetInactiveComponents(APIView):
    def get_object(self, pk):
        try:
            return HomeComponents.objects.get(pk=1)
        except HomeComponents.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = HomeComponentsSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = HomeComponentsSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class GetActiveComponents(APIView):
    def get_object(self, pk):
        try:
            return HomeComponents.objects.get(pk=2)
        except HomeComponents.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = HomeComponentsSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = HomeComponentsSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
