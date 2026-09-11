from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, filters, generics
from .models import Phone, Phone_Parts, PhoneReview, Accessory, Brand, Color
from .serializers import PhoneSerializer, RegisterSerializer, LoginSerializer, Phone_PartsSerialisers, CPhoneReviewSerializers, AccessorySerializer, BrandSerializer, ColorSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg
from .filter import PhoneFilter, AccessoryFilter    
from django_filters.rest_framework import DjangoFilterBackend
from .models import Accessory
from .serializers import AccessorySerializer
from .filter import AccessoryFilter

class AccessoryListView(generics.ListAPIView):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccessoryFilter

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = AccessoryFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class PhoneListCreateView(ListCreateAPIView):
    queryset = Phone.objects.annotate(avg_rating=Avg('reviews__rating'))
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PhoneFilter

    search_fields = ['title']
    ordering_fields = ['price', 'created_at', 'avg_rating']

class PhoneRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

class PhonePartsListCreateView(ListCreateAPIView):
    queryset = Phone_Parts.objects.all()
    serializer_class = Phone_PartsSerialisers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class PhonePartsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Phone_Parts.objects.all()
    serializer_class = Phone_PartsSerialisers

class PhoneReviewListCreateView(ListCreateAPIView):
    queryset = PhoneReview.objects.all()
    serializer_class = CPhoneReviewSerializers

class PhoneReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = PhoneReview.objects.all()
    serializer_class = CPhoneReviewSerializers



# class PhoneViewSet(viewsets.ModelViewSet):
#     queryset = Phone.objects.all()
#     serializer_class = PhoneSerializer
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filterset_class = PhoneFilter  
#     search_fields = ['title']

# class AccessoryViewSet(viewsets.ModelViewSet):
#     queryset = Accessory.objects.all()
#     serializer_class = AccessorySerializer
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filterset_class = AccessoryFilter 
#     search_fields = ['title', 'description']


@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        return Response({'message': 'logout successful'})
    return Response({'message': 'no user logged in'})


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'login successful',
            'token': token.key
        })
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'successful',
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# @api_view(['GET', 'POST'])
# def phone_list(request):
#     phones = Phone.objects.all()
#     paginator = PageNumberPagination()
#     paginator.page_size = 4
#     page = paginator.paginate_queryset(phones, request)
#     serializer = PhoneSerializer(page, many=True)
#     return paginator.get_paginated_response(serializer.data)


# @api_view(['GET'])
# def phone_list_all(request):
#     phones = Phone.objects.all()
#     serializer = PhoneSerializer(phones, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def phone_create(request):
#     serializer = PhoneSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


# @api_view(['PUT'])
# def phone_update(request, pk):
#     try:
#         phone = Phone.objects.get(pk=pk)
#     except Phone.DoesNotExist:
#         return Response({'message': 'Telefon topilmadi'}, status=404)
        
#     serializer = PhoneSerializer(phone, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


# @api_view(['GET'])
# def phone_detail(request, pk):
#     try:
#         phone = Phone.objects.get(pk=pk)
#     except Phone.DoesNotExist:
#         return Response({'message': 'Telefon topilmadi'}, status=404)
        
#     serializer = PhoneSerializer(phone)
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def phone_delete(request, pk):
#     try:
#         phone = Phone.objects.get(pk=pk)
#     except Phone.DoesNotExist:
#         return Response({'message': 'Telefon topilmadi'}, status=404)
        
#     phone.delete()
#     return Response({'message': 'The phone was deleted'})