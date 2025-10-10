from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializers import (
    RegisterSerializer, ChangePasswordSerializer, HomeSerializer, ReviewSerializer, ReviewWithHomeSerializer,
    HomeWithReviewStatsSerializer, ProfilePhotoSerializer
)
from .models import Home, Review
from django.db.models import Avg, Count, Q

class RegisterView(APIView):
    def post(self, request):
        # Endpoint to create an user 
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Endpoint to change the password of a user. User has to be logged in
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

class CreateHomeAndReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Create review and the home which the review is about, in case the home doesn't exist yet.
        # Duplicate homes are prevented
        user = request.user
        home_data = request.data.get('home')
        review_data = request.data.get('review')
        # At user ID to the data that will be stored on database
        home_data['user'] = user.pk
        review_data['user'] = user.pk

        if not home_data or not review_data:
            return Response({'error': 'Se requieren datos de home y review.'},
                            status=status.HTTP_400_BAD_REQUEST)

        home_serializer = HomeSerializer(data=home_data)
        home_serializer.is_valid(raise_exception=True)
        validated_home = home_serializer.validated_data

        review_serializer = ReviewSerializer(data=review_data)
        review_serializer.is_valid(raise_exception=True)
        validated_review = review_serializer.validated_data

        with transaction.atomic():
            # Create home and review together, or create nothing in case of error

            home_lookup = {
                # These are the fields that should be unique for a home
                'address': validated_home['address'],
                'number': validated_home['number'],
                'floor': validated_home['floor'],
                'city': validated_home['city'],
            }

            home, created = Home.objects.get_or_create(
                defaults={
                    # Fields used for creating a home when it doesn't exist by the unique fields
                    'zip_code': validated_home['zip_code'],
                    'town': validated_home['town'],
                    'user': user, 
                    'country': validated_home['country'],
                },
                **home_lookup
            )

            review = Review.objects.create(
                user=user,
                home=home,
                rating=validated_review['rating'],
                description=validated_review['description'],
                noise_level=validated_review.get('noise_level'),
                disturbance_level=validated_review.get('disturbance_level')
            )

        return Response({
            'home': HomeSerializer(home).data,
            'home_created': created,
            'review': ReviewSerializer(review).data
        }, status=status.HTTP_201_CREATED)
    
    
class ReviewViewSet(viewsets.ModelViewSet):
    # CRUD endpoint for reviews
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class HomesWithUserReviewsView(ListAPIView):
    # Read endpoint to get the reviews of the logged in user, including the related home
    serializer_class = ReviewWithHomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Home is joined because it is serialized for each review
        return Review.objects.filter(user=self.request.user).select_related('home') 
    

class HomesView(ListAPIView):
    # Read endpoint to search homes by city or town and get review stats for each home
    serializer_class = HomeWithReviewStatsSerializer
    
    def get_queryset(self):
        params = self.request.query_params
        homes = Home.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).annotate(
            avg_noise_level=Avg('reviews__noise_level')
        ).annotate(
            avg_disturbance_level=Avg('reviews__disturbance_level')
        ).annotate(
            reviews_count=Count('reviews')
        ).filter(
            reviews_count__gte=1
        )
        search_value = params.get('search')

        if search_value:
            # Search value is a query param provided by the frontend
            homes = homes.filter(Q(city__iexact=search_value) | Q(town__iexact=search_value)) 

        return homes

class ProfilePhotoView(RetrieveUpdateAPIView):
    # Endpoint to get or update (PATCH) the profile photo of the logged in user
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
