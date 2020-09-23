from rest_framework import serializers
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.models import User
from events.models import Event,Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username']


class UpcomingEventsSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-event-detail",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    class Meta:
        model = Event
        fields = ['name','start','location','img','detail']

class EventDetailSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    class Meta:
        model = Event
        fields = ['organizer', 'name', 'description','start','end','location','limit','img']

