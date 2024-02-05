from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

from .models import V2ray, Operator
from .serializers import V2raySerializer, OperatorSerializer

class OperatorAPIView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        queryset = Operator.objects.all()
        serializer = OperatorSerializer(queryset, many=True)

        res = {
            "response": "success",
            "product_type": "v2ray",
            "data": serializer.data,
        }
        return Response(res, status=status.HTTP_200_OK)

class V2rayAPIView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        queryset = V2ray.objects.all()
        serializer = V2raySerializer(queryset, many=True)
        
        res = {
            "response": "success",
            "product_type": "v2ray",
            "data": serializer.data,
        }
        return Response(res, status=status.HTTP_200_OK)
