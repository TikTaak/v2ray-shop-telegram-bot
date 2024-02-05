from rest_framework import serializers
from .models import V2ray, Operator


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = (
            "__all__"
        )
        
        
class V2raySerializer(serializers.ModelSerializer):
    operator = OperatorSerializer(Operator, many=True)
    class Meta:
        model = V2ray
        fields = (
            "__all__"
        )
        