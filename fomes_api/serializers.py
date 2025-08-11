from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Home, Review

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is wrong.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user    

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'
        read_only_fields = ['customer', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'home']
        

class HomeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = [
            'id', 'address', 'number', 'zip_code', 'city', 'town',
            'country'
        ]

class ReviewWithHomeSerializer(serializers.ModelSerializer):
    home = HomeBasicSerializer()

    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'description', 'noise_level',
            'disturbance_level', 'created_at', 'home'
        ]


