from flyapp.models import Product, PromoCode, Reviews, Subscriber, Order
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from .serializers import OrderSerializer, ReviewSerializer, EmailSerializer, PromoCodeSerializer
import razorpay
from decouple import config


class ApplyPromoCodeView(APIView):
    serializer_class = PromoCodeSerializer
    model = PromoCode

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        promo_code = self.request.GET.get("promo_code", None)

        try:
            code = PromoCode.objects.get(promo_code=promo_code)
            total = product.price
            discount = code.discount
            percentage = total * (discount / 100)

            response = {
                "total": total - percentage,
                "discount": discount,
                "percentage": percentage,

                "message": "Promocode applied"
            }
            return Response(response)

        except PromoCode.DoesNotExist:
            return Response({"error": "Invalid promocode"}, status=400)




class BillDetailsView(APIView):
    serializer_class = OrderSerializer
    model = Order

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            client = razorpay.Client(auth=(config('key_id'), config('key_secret')))
            total = order.total
            total = total * 100

            DATA = {

                "amount": int(total),
                "currency": "INR",
                "receipt": str(order.id),
                "notes": {
                    "product_id": order.product.id,
                    "product_name": order.product.product_name
                }
            }
            try:
                cile = client.order.create(data=DATA)
                order.razorpay_order_id = cile['id']
                order.save()
                return Response(data={
                    'key_id': config('key_id'),
                    'amount': int(total),
                    'order_id': order.razorpay_order_id,
                    'name': "Infly",
                    'description': f"{order.product.product_name} {order.product.id}",
                    'customer_name': f"{order.first_name} {order.last_name}",
                    'contact': f"{order.phone}",
                    'email': f"{order.email}",
                    'address': f"{order.address}, {order.city}, {order.region}, {order.country}, {order.zip_code}",



                })
            except KeyError:
                return Response({'msg': 'something went wrong'}, status=400)


class ReviewForm(CreateAPIView):
    serializer_class = ReviewSerializer
    model = Reviews


class EmailAPIView(CreateAPIView):
    serializer_class = EmailSerializer
    model = Subscriber

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        email = request.data.get("email")

        if Subscriber.objects.filter(email=email).exists():
            return Response({"msg": "already exists"})
        else:
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "subscribed"})
            else:
                return Response(data=serializer.errors, status=400)


