from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


# Create your models here.

class Product(models.Model):
    OPTIONS = (
        ('all', 'All',),
        ('digital-influence', 'Digital Influence',),
        ('courses', 'courses',),
        ('software', 'software')
    )
    category_name = models.CharField(max_length=120, choices=OPTIONS, default='software')
    product_name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images')
    desc = RichTextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product.product_name


def validate_decimal(value):
    if value < 0:
        raise ValidationError("Value must be greater than or equal to zero.")
    elif value > 100:
        raise ValidationError("value must be less than or equal to hundered")


class PromoCode(models.Model):
    promo_code = models.CharField(unique=True, max_length=20)
    discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_decimal])
    influencer_name = models.CharField(max_length=120)

    @property
    def claim(self):
        order = Order.objects.filter(promo_code=self.promo_code,status='success')
        return order.count()

    @property
    def processing(self):
        order = Order.objects.filter(promo_code=self.promo_code,status='processing')
        return order.count()



    def __str__(self):
        return self.promo_code


class Order(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=120)
    city = models.TextField()
    country = models.TextField()
    region = models.TextField()
    zip_code = models.IntegerField()
    phone = models.CharField(max_length=11)
    promo_code = models.CharField(max_length=20, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=256, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=256, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=256, blank=True, null=True)
    options = (
        ('pending','Pending'),
        ('success', 'Success'),
        ('processing', 'Processing'),
        ('failed', 'Failed'),
    )
    status = models.CharField(max_length=120,choices=options,default="pending")

    def __str__(self):
        return self.first_name

    @property
    def total(self):
        if self.promo_code:
            code = PromoCode.objects.get(promo_code=self.promo_code)
        else:
            code = None
        total = self.product.price
        if code:
            discount = code.discount
            percentage = total * (discount / 100)
            total = total - percentage
        return total


class Reviews(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rating = models.PositiveIntegerField()
    mssg = models.TextField()
    approval = models.BooleanField(default=False)

    @property
    def ratings(self):
        return range(self.rating)

    def __str__(self):
        return str(self.mssg)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email





