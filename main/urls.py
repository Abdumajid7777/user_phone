from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register,login,logout,AccessoryViewSet,BrandViewSet,
    ColorViewSet,PhoneViewSet,CartViewSet,FavoriteViewSet,OrderViewSet,
    ReviewCreateListAPIView,ApplyCouponAPIView,NotificationViewSet,StatisticsAPIView
)

router = DefaultRouter()
router.register(r'accessories', AccessoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'color', ColorViewSet)
router.register(r'phone', PhoneViewSet, basename='phone')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('reviews/', ReviewCreateListAPIView.as_view(), name='review-list-create'),
    path('coupons/apply/', ApplyCouponAPIView.as_view(), name='apply-coupon'),
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
]