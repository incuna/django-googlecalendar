from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from forms import AddEventForm, AddEventCalendarForm
from models import Calendar, Event

def googlecalendar_list(request, extra_context=None, template_name='googlecalendar/calendar_list.html'):
    context = RequestContext(request)
    if extra_context is not None:
        context.update(extra_context)

    calendars = Calendar.active.all()
    if not len(calendars):
        raise Http404

    event_form = None
    if settings.USER_ADD_EVENTS:
        event_form = AddEventForm()

        if request.method == 'POST':
            event_form = AddEventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                if request.user.is_authenticated():
                    event.user = request.user
                event.save()

                event_form = AddEventForm()
                messages.add_message(request, messages.INFO, _('New event was successfully saved'))

    context.update({'object_list': Calendar.active.all(), 'event_form': event_form})
    return render_to_response(template_name, context)

def googlecalendar(request, slug, extra_context=None, template_name='googlecalendar/calendar_detail.html'):
    context = RequestContext(request)
    if extra_context is not None:
        context.update(extra_context)

    calendar = get_object_or_404(Calendar.active, slug=slug)

    event_form = None
    if settings.USER_ADD_EVENTS:
        event_form = AddEventCalendarForm(calendar=calendar)

        if request.method == 'POST':
            event_form = AddEventCalendarForm(request.POST, calendar=calendar)
            if event_form.is_valid():
                event_form.save()
                event_form = AddEventCalendarForm(calendar=calendar)
                messages.add_message(request, messages.INFO, _('New event was successfully saved'))

    context.update({'object': calendar, 'event_form' : event_form})
    return render_to_response(template_name, context)

def googlecalendar_event(request, calendar, event, extra_context=None, template_name='googlecalendar/event_detail.html'):
    context = RequestContext(request)
    if extra_context is not None:
        context.update(extra_context)

    context.update({'object': get_object_or_404(Event.objects.active(), slug=event)})
    return render_to_response(template_name, context)

