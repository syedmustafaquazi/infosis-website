from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'company', 'email', 'mobile', 'service', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    ordering = ('-created_at',)
