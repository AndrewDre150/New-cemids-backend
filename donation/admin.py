from django.contrib import admin
from .models import Donation

admin.site.site_header = "CEMIDS Administration"
admin.site.site_title = "Cemids Admin"
admin.site.index_title = "Welcome to Cemids Admin"

class DonationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'amount')  # Fields to display in the admin list
    search_fields = ('full_name', 'email', 'phone_number')  # Fields for searching donations

admin.site.register(Donation, DonationAdmin)
