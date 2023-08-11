from django.urls import path
from flyapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<str:category_name>/', views.ProductListView.as_view(), name='product'),
    path('checkout/<int:id>', views.CheckoutView.as_view(), name='checkout'),
    path('payment/success/', views.success, name='success'),
    path('payment/error/', views.error, name='error'),
    path('payment-callback/', views.paymentcallback, name='payment'),
    path('payment/processing',views.processing, name='processing')

]
