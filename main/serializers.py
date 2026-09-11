from rest_framework import serializers
from .models import Phone, Phone_Parts, PhoneReview, Brand, Color
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Accessory, Phone


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'year']  

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']  

class PhoneSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    color = serializers.StringRelatedField()

    class Meta:
        model = Phone
        fields = '__all__'


    brand = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Brand.objects.all()
    )
    color = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Color.objects.all(),
        many=True
    )


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


class CPhoneReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = PhoneReview
        fields = '__all__'
