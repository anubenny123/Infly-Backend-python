from django.urls import path
from flyapp.api import views
urlpatterns=[
    path('api/product/<int:pk>/',views.ApplyPromoCodeView.as_view(), name='apply'),
    path('api/bill/',views.BillDetailsView.as_view(),name='bill-form'),
    path('api/review/',views.ReviewForm.as_view(),name='review'),
    path('api/email/',views.EmailAPIView.as_view(),name='email'),

]