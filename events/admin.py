from django.contrib import admin
from .models import Event,Booking


admin.site.site_header = "DJANGO EVENT PLANNER"
admin.site.site_title = "dashboard"
admin.site.index_title = "Organizer Dashboard"

class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'location','start','end','limit','organizer']
    list_display = ['name', 'location','start','end','limit']
    list_filter = ['organizer']
    search_fields = ['name', 'location','start','end','limit']
    list_editable = ['limit']
    list_display_links = ['name']


class BookingAdmin(admin.ModelAdmin):
    fields = ['customer', 'event','tickets']
    list_display = ['customer', 'event','tickets','time']
    list_filter = ['event']
    search_fields = ['customer', 'event']
    list_display_links = ['customer']


admin.site.register(Event,EventAdmin)
admin.site.register(Booking,BookingAdmin)