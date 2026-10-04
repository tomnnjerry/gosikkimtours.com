from django.contrib import admin

from .models import Enquiry, Subscriber


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("created", "name", "email", "phone", "contact_pref", "kind", "lands", "month", "travellers", "handled")
    list_filter = ("handled", "kind", "contact_pref", "month")
    search_fields = ("name", "email", "lands", "message")
    list_editable = ("handled",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("created", "email", "source_page")
    search_fields = ("email",)
