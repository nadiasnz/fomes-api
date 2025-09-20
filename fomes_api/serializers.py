from rest_framework import serializers
from .models import Home, Review, FomesUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = FomesUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return FomesUser.objects.create_user(**validated_data)


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
            'id', 'address', 'number', 'floor', 'zip_code', 'city', 'town',
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


class HomeWithReviewStatsSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    avg_noise_level = serializers.FloatField(read_only=True)
    avg_disturbance_level = serializers.FloatField(read_only=True)
    

    class Meta:
        model = Home
        fields = [
            'id', 'address', 'number', 'floor', 'zip_code', 'city',
            'town', 'country', 'reviews_count', 'avg_rating', 'avg_noise_level', 'avg_disturbance_level'
        ]

class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FomesUser
        fields = ["photo"]