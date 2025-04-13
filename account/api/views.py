from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import UserSerializer
from account.models import User

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

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  # Assuming you want authenticated access
    


        

        