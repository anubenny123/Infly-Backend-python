from django.contrib.auth.models import User
from flyapp.models import Product,PromoCode,Subscriber,Order,Reviews
from rest_framework import serializers


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "category_name",
            "product_name",
            "image",
            "desc",
            "price",
            "featured",
        ]


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['name', 'email', 'rating', 'mssg']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscriber
        fields="__all__"
