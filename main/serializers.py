from rest_framework import serializers
from .models import Phone, Phone_Parts, PhoneReview, Brand, Color, Accessory, Cart, CartItem, Order, OrderItem, Favorite
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'phone', 'accessory', 'created_at']
        read_only_fields = ['user', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.phone:
            representation['phone'] = PhoneSerializer(instance.phone).data
        if instance.accessory:
            representation['accessory'] = AccessorySerializer(instance.accessory).data
        return representation

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = ['id', 'accessory_type', 'price', 'description', 'image']

# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ['id', 'user', 'phone', 'accessory', 'created_at']
#         read_only_fields = ['user', 'created_at']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if instance.phone:
#             representation['phone'] = PhoneSerializer(instance.phone).data
#         if instance.accessory:
#             representation['accessory'] = AccessorySerializer(instance.accessory).data
#         return representation

class CartItemSerializer(serializers.ModelSerializer):
    phone_title = serializers.ReadOnlyField(source='phone.title')
    phone_price = serializers.ReadOnlyField(source='phone.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'phone', 'phone_title', 'phone_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.phone.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_cart_price']

    def get_total_cart_price(self, obj):
        return sum(item.phone.price * item.quantity for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    phone_title = serializers.ReadOnlyField(source='phone.title')

    class Meta:
        model = OrderItem
        fields = ['id', 'phone', 'phone_title', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'year']  

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']  

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        
        if user is None:
            raise serializers.ValidationError(
                'invalid passwor or username'
            )
        data['user'] = user
        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class Phone_PartsSerialisers(serializers.ModelSerializer):

    class Meta:
        model = Phone_Parts
        fields = '__all__'

class PhoneReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = PhoneReview
        fields = '__all__'
