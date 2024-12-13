from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    total_tickets = models.PositiveIntegerField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    selected_seats = models.JSONField(default=list, blank=True)  # Список місць із побажаннями
    purchase_date = models.DateTimeField(auto_now_add=True)
    preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.event.name}"
