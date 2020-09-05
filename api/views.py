from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.authtoken.models import Token
from login import models
from login.models import UserDetails as ud
import requests


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Registration(APIView):
    def post(self, request):
        data = request.data
        print(data)
        user = models.UserDetails(name=data['name'], username=data['username'], password=data['password'],
                                  phone=data['phone'], email=data['email'], perms=data['perms'],
                                  ref=data['ref'], role=data['role'], status=1, team=data['team'])
        user.save()
        print(user.email)
        token = Token.objects.create(user=user)
        return Response({"token": token.key})


class TokenGen(APIView):
    def post(self, request):
        data = request.data
        print("Data Decoded")
        user = models.UserDetails.objects.get(username=data['name'])
        print("Data Saved")
        token = Token.objects.get(user=user)
        return Response({'token': token.key})


class Verify(APIView):
    def post(self, request):
        data = request.data
        details = models.UserDetails.objects.filter(token=data['token']).exists()
        print(details)
        if details == True:
            return Response({'exists': 'true'})
        else:
            return Response({'exists': 'false'})






