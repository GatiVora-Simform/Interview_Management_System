from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.api.serializers import UserSerializer
from account.models import User
from interview.api.permissions import IsAdmin, AdminFullInterviewerReadOnly, IsCandidate

# @api_view(['POST'])
# def registration_view(request):
    
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'successfully registered new user'
#             data['email'] = user.email
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             data = serializer.errors
#             return Response(data)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    permission_classes = [AllowAny]

class UserListView(generics.ListAPIView):
    """
    Admin-only endpoint to list all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminFullInterviewerReadOnly]
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    This view is used for users to access and update their own profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

        

        