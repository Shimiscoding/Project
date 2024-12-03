from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Event, RSVP
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from .models import Event

# View to display the list of events
def event_list(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'events/event_list.html', {'events': events})

def event_list_student(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'events/event_list_student.html', {'events': events})

# View to show details of a single event, including RSVP functionality

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Check if the user has already RSVP'd
    rsvp = RSVP.objects.filter(event=event, user=request.user).first()

    if request.method == 'POST':
        # Toggle the RSVP status (attending or not attending)
        if rsvp:
            rsvp.attending = not rsvp.attending  # Toggle the attending status
            rsvp.save()
        else:
            # If the user hasn't RSVP'd yet, create a new RSVP entry
            RSVP.objects.create(event=event, user=request.user, attending=True)

        return redirect('event_detail', pk=event.pk)  # Redirect back to the event detail page

    # Fetch all attendees
    attendees = RSVP.objects.filter(event=event, attending=True)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'rsvp': rsvp,
        'attendees': attendees,
    })


def event_detail_student(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Check if the user has already RSVP'd
    rsvp = RSVP.objects.filter(event=event, user=request.user).first()

    if request.method == 'POST':
        # Toggle the RSVP status (attending or not attending)
        if rsvp:
            rsvp.attending = not rsvp.attending  # Toggle the attending status
            rsvp.save()
        else:
            # If the user hasn't RSVP'd yet, create a new RSVP entry
            RSVP.objects.create(event=event, user=request.user, attending=True)

        return redirect('event_detail_student', pk=event.pk)  # Redirect back to the event detail page

    # Fetch all attendees
    attendees = RSVP.objects.filter(event=event, attending=True)

    return render(request, 'events/event_detail_student.html', {
        'event': event,
        'rsvp': rsvp,
        'attendees': attendees,
    })
# View to provide event data in a format that can be used in a calendar (JSON response)
def calendar_view(request):
    events = Event.objects.all()

    # Format events for FullCalendar
    calendar_data = [
        {
            'title': event.title,
            'start': event.start_time.isoformat(),  # ISO format
            'end': event.end_time.isoformat() if event.end_time else None,
            'description': event.description,
        }
        for event in events
    ]

    return render(request, 'events/calendar_view.html', {'events': calendar_data})

def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')

        # Create and save the new event
        event = Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            created_at=timezone.now()
        )
        event.save()
        return redirect('event_list')  # Redirect to the list of events after saving

    return render(request, 'events/create_event.html')  # Render the event creation page