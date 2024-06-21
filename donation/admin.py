from django.contrib import admin
from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'amount')  # Fields to display in the admin list
    search_fields = ('full_name', 'email', 'phone_number')  # Fields for searching donations

admin.site.register(Donation, DonationAdmin)
