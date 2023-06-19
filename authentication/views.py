from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import UserSerializer, RefreshTokenSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

# Create your views here.


@api_view(["GET"])
def index(request):
    return Response({"Hello": "World"})


@api_view(["POST"])
def register_new_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            payload = {
                "id": serializer.data["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow(),
            }

            token = jwt.encode(payload, "secret", algorithm="HS256")

            response = Response()

            response.set_cookie(key="auth", value=token, httponly=True)
            return Response(
                {
                    "email": serializer.data["email"],
                    "user_id": serializer.data["id"],
                    "token": token,
                    "refresh_token": "secret",
                }
            )
        return Response(
            {
                "message": "Some Error",
                "description": "Form is correct, make sure you are sending all the valid entries",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"message": "Some", "description": e}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def sign_in_user(request):
    email = request.data["email"]
    password = request.data["password"]
    user = User.objects.filter(email=email).first()
    if user is None:
        raise AuthenticationFailed("User not found")
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password!")
    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, "secret", algorithm="HS256")

    response = Response()

    response.set_cookie(key="auth", value=token, httponly=True)
    response.data = {
        "email": user.email,
        "user_id": user.id,
        "token": token,
        "refresh_token": "secret",
    }
    return response

@api_view(["POST"])
def refresh_auth_token(request):
    serializer = RefreshTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        payload= jwt.decode(serializer.data["token"], "secret", algorithms=["HS256"])
                    
    return Response({"Hello": "World"})
