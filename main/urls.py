from django.urls import path,include
from smart_selects import urls as smart_selects_urls
from rest_framework.routers import DefaultRouter
from .views import AccessoryViewSet, BrandViewSet, ColorViewSet
from .views import (
    register,
    login,
    logout,
    PhoneListCreateView,
    PhoneRetrieveUpdateDestroyAPIView,
    PhonePartsListCreateView
)

router = DefaultRouter()
router.register(r'accessories', AccessoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'color', ColorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('chaining/', include(smart_selects_urls)),
    path('phone/', PhoneListCreateView.as_view(), name='phone-list-create'),
    path('phone/<int:pk>/', PhoneRetrieveUpdateDestroyAPIView.as_view(), name='phone-detail'),
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