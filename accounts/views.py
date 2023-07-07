from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from stadium_app.permissions import IsAdmin
from . models import CustomUser


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        try:
            user = CustomUser.objects.create_user(username=username, role=role)
            user.set_password(password)
            user.save()
            return Response({
                'message': f'User "{username}" created successfully!'
            }, status=201)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=400)

