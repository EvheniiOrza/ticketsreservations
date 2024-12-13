import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Event, Ticket
from .forms import TicketPurchaseForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    from django.http import JsonResponse  # Додатково для перевірки у випадку помилок

    event = get_object_or_404(Event, id=event_id)
    booked_seats = (
        Ticket.objects.filter(event=event)
        .values_list('selected_seats', flat=True)
    )

    # Розпаковуємо всі місця з JSON-поля `selected_seats`
    booked_seats_flat = []
    for seats_json in booked_seats:
        booked_seats_flat.extend(seats_json)  # Додаємо всі місця у фінальний список

    seats_range_row1 = range(1, 27)
    seats_range_row2 = range(27, 53)

    if request.method == 'POST':
        try:
            selected_seats = request.POST.get('selected_seats')
            import json
            selected_seats = json.loads(selected_seats)  # Перетворюємо JSON у Python-об'єкти

            for seat in selected_seats:
                Ticket.objects.create(
                    event=event,
                    selected_seats=[seat["seat"]],  # Додаємо місце як список
                    preferences=seat["preferences"],  # Зберігаємо побажання
                )

            return redirect('event_detail', event_id=event.id)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

    return render(request, 'event_detail.html', {
        'event': event,
        'booked_seats': booked_seats_flat,  # Передаємо розпаковані заброньовані місця
        'seats_range_row1': seats_range_row1,
        'seats_range_row2': seats_range_row2,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})