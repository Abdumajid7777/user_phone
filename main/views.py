from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from .models import (
    Phone, Accessory, Brand, Color, Cart,  
    Order, Favorite, Review, Notification, Coupon
)
from .serializers import (
    PhoneSerializer, AccessorySerializer, BrandSerializer, ColorSerializer,
    ReviewSerializer, OrderSerializer, NotificationsSerializer,
    CartSerializer, FavoriteSerializer, LoginSerializer, RegisterSerializer
)

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brand', 'color']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewCreateListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplyCouponAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            coupon = Coupon.objects.get(code=code)
            if not coupon.is_valid():
                return Response({"error": "Купон амал қилиш муддати тугаган ёки фаол эмас."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Купон муваффақиятли қўшилди!", "discount": coupon.discount_percent}, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({"error": "Бундай купон мавжуд эмас."}, status=status.HTTP_404_NOT_FOUND)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class StatisticsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_phones = Phone.objects.count()
        total_orders = Order.objects.count()
        total_sales = Order.objects.aggregate(sum_price=Sum('total_price'))['sum_price'] or 0

        data = {
            "total_phones": total_phones,
            "total_orders": total_orders,
            "total_sales": total_sales
        }
        return Response(data, status=status.HTTP_200_OK)


class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



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

