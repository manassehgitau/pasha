from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, TokenSerializer, ProfileSerializer, FollowerSerializer
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Profile, Follower

def index(request):
    return HttpResponse('My app is running!')

@swagger_auto_schema(   
    method='POST',  
    request_body=UserRegistrationSerializer,    
    responses={201: 'User created', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='POST',  
    request_body=TokenSerializer,    
    responses={200: 'Login successful', 400: 'Bad Request', 401: 'Invalid credentials'}
)
@api_view(['POST'])
@permission_classes([AllowAny]) 
def login(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET', 
    responses={
        200: ProfileSerializer,
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Profile Not Found'
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)



@swagger_auto_schema(
    method='PATCH', 
    request_body=ProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Profile Not Found'
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()  
        return Response({
            "message": "Profile updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        "message": "Profile update failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='POST',
    responses={
        201: 'User followed successfully',
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'User Not Found'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a specific user.
    """
    followed_user = get_object_or_404(User, pk=user_id)
    if request.user == followed_user:
        return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Follower.objects.filter(follower=request.user, followed=followed_user).exists():
        return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

    follower_relation = Follower.objects.create(follower=request.user, followed=followed_user)
    serializer = FollowerSerializer(follower_relation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='DELETE',
    responses={
        204: 'User unfollowed successfully',
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'User Not Found'
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a specific user.
    """
    followed_user = get_object_or_404(User, pk=user_id)
    if request.user == followed_user:
        return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    
    follow_relation = get_object_or_404(Follower, follower=request.user, followed=followed_user)
    follow_relation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='GET',
    responses={
        200: FollowerSerializer(many=True),
        401: 'Unauthorized',
        404: 'Not Found'
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_followers(request, user_id):
    """List all followers for a specific user."""
    user = get_object_or_404(User, pk=user_id)
    followers = get_list_or_404(Follower, followed=user)
    serializer = FollowerSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    responses={
        200: ProfileSerializer(many=True),
        401: 'Unauthorized'
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """Search for users by username or email."""
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
        profiles = [user.profile for user in users if hasattr(user, 'profile')]
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    return Response([], status=status.HTTP_200_OK)