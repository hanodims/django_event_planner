from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter,OrderingFilter

from django.utils.timezone import now

from events.models import Event,Booking
from .permissions import IsOrganizer,IsBooker
from .serializers import (
	EventsSerializer,EventDetailSerializer,MyBookingsSerializer,
	UserCreateSerializer,UserLoginSerializer,EventCreateSerializer,
	BookersSerializer,BookingsSerializer,BookingsSerializer_2
)


#As an event organizer/user I can signup.
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


#As an event organizer/user I can login
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

#List of all upcoming events
class UpcomingEventsList(ListAPIView):
	queryset = Event.objects.filter(start__gt=now())
	serializer_class = EventsSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	search_fields = ['name']
	permission_classes = [AllowAny]


class EventDetail(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [AllowAny]

#List of events for a specific organizer
class MyEventsList(ListAPIView):
	serializer_class = EventsSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	permission_classes = [IsOrganizer]

	def get_queryset(self):
		return Event.objects.filter(organizer=self.request.user)

#List of events I have booked for, as a logged in user
class MyBookingList(ListAPIView):
	serializer_class = MyBookingsSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	permission_classes = [IsAuthenticated,IsBooker]

	def get_queryset(self):
		return Booking.objects.filter(customer=self.request.user)


#As an event organizer I can create an event.
class EventCreate(CreateAPIView):
	serializer_class = EventCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)

#As an event organizer I can update an event.
class EventUpdate(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsOrganizer]

#As an event organizer I can retrieve a list of people who have booked for an event.
class Bookers(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = BookersSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsOrganizer]


#As a user I can book for an event.
class BookingEvent(CreateAPIView):
	serializer_class = BookingsSerializer_2
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		event_obj = Event.objects.get(id=self.kwargs['event_id'])
		if Booking.objects.filter(customer=self.request.user,event=event_obj):
			raise exceptions.ParseError({"error":["You Are Already In"]})
		if event_obj.limit > 0:
			event_obj.limit -= serializer.validated_data['tickets']
			event_obj.save()
			return serializer.save(customer=self.request.user, event_id=self.kwargs['event_id'])#?
		else:
			raise exceptions.ParseError({"error":["No More tickets"]})

