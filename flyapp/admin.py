from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Reviews)
admin.site.register(Images)
admin.site.register(Subscriber)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'influencer_name','discount', 'display_claim','display_processing')

    def display_claim(self, obj):
        return obj.claim

    display_claim.short_description = 'Claim Count'

    def display_processing(self,obj):
        return obj.processing

admin.site.register(PromoCode,ModelAdmin)