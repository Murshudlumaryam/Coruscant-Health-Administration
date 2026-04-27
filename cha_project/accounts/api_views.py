from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'administrator' or request.user.is_superuser)

class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('doctor','administrator') or (request.user.is_authenticated and request.user.is_superuser)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_register(request):
    s = UserRegistrationSerializer(data=request.data)
    if s.is_valid():
        user = s.save()
        return Response({'message': 'Registration submitted. Awaiting approval.', 'id': user.id}, status=status.HTTP_201_CREATED)
    return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    if user.role in ('patient','doctor') and not user.is_approved:
        return Response({'error': 'Account pending approval'}, status=status.HTTP_403_FORBIDDEN)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })

@api_view(['GET'])
def api_me(request):
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@permission_classes([IsAdminRole])
def api_pending_users(request):
    users = User.objects.filter(is_approved=False, role__in=['patient','doctor'])
    return Response(UserSerializer(users, many=True).data)

@api_view(['POST'])
@permission_classes([IsAdminRole])
def api_approve_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_approved = True
        user.save()
        return Response({'message': f'{user.get_full_name()} approved.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    def get_queryset(self):
        role = self.request.query_params.get('role')
        qs = User.objects.all()
        if role:
            qs = qs.filter(role=role)
        return qs
