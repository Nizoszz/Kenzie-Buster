from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({"detail": "No active account found with the given credentials"},
                            status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)

        token_dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(token_dict, status.HTTP_200_OK)


class UserView(APIView):
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if "is_superuser" in request.data:
            request.data.pop("is_superuser")
        if "is_employee" in request.data and request.data["is_employee"]: 
            request.data["is_superuser"] = True
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserViewDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        if user.id == user_id and user.is_employee is False or user.is_employee and user.id != user_id:
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"detail": "No active account found with the given credentials"},
                            status.HTTP_403_FORBIDDEN)
        
    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        if user.id == user_id and user.is_employee is False or user.is_employee and user.id != user_id:
            serializer = UserSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"detail": "No active account found with the given credentials"},
                            status.HTTP_403_FORBIDDEN)
