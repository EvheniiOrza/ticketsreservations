from django.contrib import admin
from .models import Event, Ticket

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'total_tickets', 'price_per_ticket')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'buyer_name', 'preferences', 'purchase_date', 'get_preferences')

    def get_preferences(self, obj):
        return obj.preferences
    get_preferences.short_description = "Побажання"
