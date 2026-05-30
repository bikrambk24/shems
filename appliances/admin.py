from django.contrib import admin

from appliances.models import Appliance


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ['name', 'appliance_type', 'owner', 'power_rating_kw', 'is_on', 'is_faulty']
    list_filter = ['appliance_type', 'is_on', 'is_faulty']
    search_fields = ['name', 'owner__username']
