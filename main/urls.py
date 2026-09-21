from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register,
    login,
    logout,
    AccessoryViewSet,
    BrandViewSet,
    ColorViewSet,
    PhoneViewSet,
    CartViewSet,
    FavoriteListCreateView,
    FavoriteDetailView,
)
router = DefaultRouter()
router.register(r'accessories', AccessoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'color', ColorViewSet)
router.register(r'phone', PhoneViewSet, basename='phone')  
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:pk>/', FavoriteDetailView.as_view(), name='favorite-delete'),
]





















# from django.urls import path
# from .views import (
#     register, login, logout,
#     phone_list, phone_list_all, phone_create,
#     phone_detail, phone_update, phone_delete
#     # auto_list,
#     # auto_detail,
#     # auto_delete,
#     # auto_create,
#     # auto_update,
#     # auto_parts_list,
#     # auto_parts_detail,
#     # auto_parts_delete,
#     # auto_parts_create,
#     # auto_parts_update,
# )

# urlpatterns = [
#     # Auth endpoints
#     path('register/', register),
#     path('login/', login),
#     path('logout/', logout),

#     # Phone API endpoints
#     path('phones/', phone_list),
#     path('phones/all/', phone_list_all),
#     path('phones/create/', phone_create),
#     path('phones/<int:pk>/', phone_detail),
#     path('phones/<int:pk>/update/', phone_update),
#     path('phones/<int:pk>/delete/', phone_delete),
# ]