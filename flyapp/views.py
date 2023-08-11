from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from flyapp.models import Product, Order
from flyapp.models import Reviews
from django.http import JsonResponse
import razorpay
from decouple import config
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        full = Product.objects.filter(category_name='all').last()
        featured = Product.objects.filter(featured=True)[:4]
        reviews = Reviews.objects.filter(approval=True)
        context["full"] = full
        context["featured"] = featured
        context["reviews"] = reviews
        return context


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'product.html'

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        if category_name == 'all':
            return Product.objects.all()
        else:
            return Product.objects.filter(category_name=category_name)


class CheckoutView(DetailView):
    model = Product
    template_name = 'checkout.html'
    pk_url_kwarg = "id"


@csrf_exempt
def paymentcallback(request):
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')
    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
    except Order.DoesNotExist:
        return redirect('error')

    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_signature = razorpay_signature
    order.save()

    client = razorpay.Client(auth=(config('key_id'), config('key_secret')))

    response = client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    })
    if response == False:
        return redirect('error')

    payment_stat = client.payment.fetch(razorpay_payment_id)
    print(payment_stat['status'])
    if payment_stat['status'] == 'captured':
        order.status = 'success'
        order.save()
        return redirect('success')
    elif payment_stat['status'] == 'authorized':
        order.status = 'processing'
        order.save()
        return redirect('processing')
    elif payment_stat['status'] == 'failed':
        order.status = 'failed'
        order.save()
        return redirect('error')
    else:
        return redirect('error')


@csrf_exempt
def success(request):
    return render(request, 'success.html')


@csrf_exempt
def error(request):
    return render(request, 'error.html')


@csrf_exempt
def processing(request):
    return render(request, 'processing.html')
