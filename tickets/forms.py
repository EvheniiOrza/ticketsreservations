from django import forms
from .models import Ticket

class TicketPurchaseForm(forms.ModelForm):
    FOOD_CHOICES = [
        ('yes', 'Їжа'),
        ('no', 'Без їжі'),
    ]
    DRINK_CHOICES = [
        ('water', 'Вода'),
        ('alcohol', 'Міцні напої'),
        ('none', 'Без напоїв'),
    ]
    BEDDING_CHOICES = [
        ('yes', 'Постіль'),
        ('no', 'Без постелі'),
    ]

    food = forms.ChoiceField(choices=FOOD_CHOICES, widget=forms.RadioSelect, label="Їжа", required=False)
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.RadioSelect, label="Напої", required=False)
    bedding = forms.ChoiceField(choices=BEDDING_CHOICES, widget=forms.RadioSelect, label="Постіль", required=False)

    class Meta:
        model = Ticket
        fields = ['buyer_name', 'buyer_email']

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Кількість квитків має бути більшою за 0.")
        if self.event and quantity > self.event.total_tickets:
            raise forms.ValidationError("Недостатньо квитків для покупки.")
        return quantity

    def save(self, commit=True):
        ticket = super().save(commit=False)
        # Додаємо побажання до поля preferences
        ticket.preferences = {
            'food': self.cleaned_data.get('food'),
            'drink': self.cleaned_data.get('drink'),
            'bedding': self.cleaned_data.get('bedding'),
        }
        if commit:
            ticket.save()
        return ticket
