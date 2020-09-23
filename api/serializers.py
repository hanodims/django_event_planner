from rest_framework import serializers
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.models import User
from events.models import Event,Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username']


class EventsSerializer(serializers.ModelSerializer):
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


class MyBookingsSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['event', 'tickets', 'time']

    def get_event(self, obj):
        event_objs = Event.objects.get(id=obj.event.id)
        event_json = EventsSerializer(event_objs, many=False).data
        return  event_json 


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'description','start','end','location','limit','img']


class BookingsSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    class Meta:
        model = Booking
        fields = ['tickets', 'time','customer']


class BookingsSerializer_2(serializers.ModelSerializer):#????
    class Meta:
        model = Booking
        fields = ['tickets', 'time']


class BookersSerializer(serializers.ModelSerializer):
    bookers = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['name','start','location','img','bookers']

    def get_bookers(self, obj):
        booker_objs = Booking.objects.filter(event=obj)
        bookers_json = BookingsSerializer(booker_objs, many=True).data
        return  bookers_json


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect username/password combination! Noob..")

        return data
