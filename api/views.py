from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import UpcomingEventsSerializer,EventDetailSerializer
from rest_framework.filters import SearchFilter,OrderingFilter

from django.utils.timezone import now

from events.models import Event,Booking
from .permissions import IsOrganizer

# Create your views here.
class UpcomingEventsList(ListAPIView):
	queryset = Event.objects.filter(start__gt=now())
	serializer_class = UpcomingEventsSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	search_fields = ['name']
	permission_classes = [AllowAny]


class EventDetail(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [AllowAny]


class MyEventsList(ListAPIView):
	serializer_class = UpcomingEventsSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	permission_classes = [IsOrganizer]

	def get_queryset(self):
		return Event.objects.filter(organizer=self.request.user)