from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from database.models import User


from .serializers import *



class RegisterView(APIView):

    serializer_class = RegisterSerializers

    def post(self,request):
        serializer_class = RegisterSerializers(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()

        if serializer_class: 
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)

        return Response(serializer_class.data,status=status.HTTP_400_BAD_REQUEST)



class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializers

    def post(self, request):

        # Recupera las credenciales y autentica al usuario

        email    = request.data.get('email', None)
        password = request.data.get('password', None)
        user     = authenticate(email=email, password=password)        

        if user:            
            serializer = LoginSerializers(data=request.data)            
            if serializer.is_valid():
                return Response(
                    {'token':serializer.validated_data.get('access'),                
                    'refresh-token':serializer.validated_data.get('refresh')},

                    status=status.HTTP_200_OK)     

        return Response({'message':'Incorrect email or password.'},
            status=status.HTTP_400_BAD_REQUEST)           



class Logout(APIView):
    
    def post(self,request):

        user = User.objects.filter(id=request.data.get('user'))

        if user.exists():

            RefreshToken.for_user(user.first())
            return Response({'massage':'Sesion Cerrada de forma exitosa.'},status=status.HTTP_200_OK)
        else:
            return Response({'massage':'Usuario no encontrado.'},status=status.HTTP_400_BAD_REQUEST)    
