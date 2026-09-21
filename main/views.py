from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from .models import Phone, Phone_Parts, PhoneReview, Accessory, Brand, Color,  Cart, CartItem, Order, OrderItem, Favorite
from .serializers import( PhoneSerializer, RegisterSerializer, LoginSerializer, Phone_PartsSerialisers, PhoneReviewSerializers, AccessorySerializer, BrandSerializer, ColorSerializer, CartSerializer, OrderSerializer, FavoriteSerializer) 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg
from .filter import PhoneFilter, AccessoryFilter, PhonePriceFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .paginations import StandardResultsSetPagination

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        phones = request.data.get('phones', [])
        accessories = request.data.get('accessories', [])

        if phones or accessories:
            created_favorites = []
            
            for phone_id in phones:
                fav, created = Favorite.objects.get_or_create(
                    user=request.user, phone_id=phone_id
                )
                if created:
                    created_favorites.append(fav)

            for accessory_id in accessories:
                fav, created = Favorite.objects.get_or_create(
                    user=request.user, accessory_id=accessory_id
                )
                if created:
                    created_favorites.append(fav)

            serializer = self.get_serializer(created_favorites, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            favorites = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brand', 'color', 'condition']
    search_fields = ['title']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at'] 

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Favorite.objects.none()
            
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteDetailView(generics.DestroyAPIView):

    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)
    
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Cart.objects.none()
        return Cart.objects.filter(user=self.request.user)
    
class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AccessoryFilter
    search_fields = ['title', 'description', 'accessory_type']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

class PhonePartsListCreateView(ListCreateAPIView):
    queryset = Phone_Parts.objects.all()
    serializer_class = Phone_PartsSerialisers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class PhonePartsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Phone_Parts.objects.all()
    serializer_class = Phone_PartsSerialisers

class PhoneReviewListCreateView(ListCreateAPIView):
    queryset = PhoneReview.objects.all()
    serializer_class = PhoneReviewSerializers

class PhoneReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = PhoneReview.objects.all()
    serializer_class = PhoneReviewSerializers
# https://yummyanime.tv/7554-za-nebrezhnoj-molodoj-devushkoj-uhazhivaet-byvshij-zhenih-ee-sestry-m2.html


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

