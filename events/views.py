from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import UserSignup, UserLogin, EventForm,BookingForm
from .models import Event,Booking
from django.utils.timezone import now

def NoAccess(request):
    context = {
        "msg": 'you have no access!',
    }
    return render(request, 'noaccess.html', context)


def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid(): 

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                if request.user.is_staff:
                    return redirect('dashboard') 
                else:
                    return redirect('dashboard') 
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

#As an event organizer I have a dashboard,and see it when login
def Dashboard(request): 
    #As a user I can track previous events I have went to.
    lasts = Booking.objects.filter(customer=request.user,event__end__lt=now())
    currents = Booking.objects.filter(customer=request.user,event__start__lte=now(),event__end__gte=now())
    future = Booking.objects.filter(customer=request.user,event__start__gte=now())
    #As an event organizer I have a list of the events that I created in my dashboard
    events = Event.objects.filter(organizer=request.user)
    context = {
        "events": events,
        "last": lasts,
        "currents": currents,
        "future": future,
        'current_date' : now()
    }
    return render(request, 'dashboard.html', context)


 #As a user I can see a list of upcoming events when I log in.
 #user not able to see passed.
def UpcomingEvents(request):
    events = Event.objects.filter(start__gte=now())
    #As a user I can search for an event either by it's title, description or organiz
    query = request.GET.get("q")
    if query:
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()
    
    context = {
        "events": events,
    }
    return render(request, 'events.html', context)

#As a user I can see the full details of the event
def EventDetail(request,event_id):
    event_obj = Event.objects.get(id=event_id)
    context = {
        "event": event_obj,
        #As an event organizer I can track the users who booked for my events in my event detail view.
        "users": Booking.objects.filter(event=event_obj),
    }
    return render(request, 'detail.html', context)


#As an Event organizer I can create an Event in my dashboard
def EventCreate(request):
    if not request.user.is_authenticated:
        return redirect('no-access')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Successfull!")
            return redirect('dashboard')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)


def EventUpdate(request,event_id):
    event = Event.objects.get(id=event_id)
    if not request.user.is_authenticated and request.user != event.organizer:
        return redirect('no-access')
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES,instance=event)
        if form.is_valid():
            form.save()
            return redirect("event-detail",event_id=event_id)
            messages.success(request, "Successfull!")
    context = {
        "event":event,
        "form": form,
    }
    return render(request, 'update.html', context)

#As a user I can book for an eve
def EventBooking(request,event_id):
    event_obj = Event.objects.get(id=event_id)
    if not request.user.is_authenticated or event_obj.limit == 0 or event_obj.limit == 0 or event_obj.start < now() or event_obj.end < now():
        return redirect('no-access')
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            #As a user If an event is full, I will not be able to book.
            if book.tickets > event_obj.limit:
                messages.warning(request, f"just {event_obj.limit} left!")
                return redirect('event-booking',event_id=event_id)
            elif book.tickets <= 0:
                messages.warning(request, f"Enter correct number, {event_obj.limit} left!")
                return redirect('event-booking',event_id=event_id)
            book.customer = request.user
            book.event = event_obj
            if Booking.objects.filter(customer=book.customer,event=book.event):
                messages.success(request, "You are in already!")
                return redirect('dashboard')
            event_obj.limit -= book.tickets
            event_obj.save()
            book.save()
            messages.success(request, "Successfull!")
            return redirect('dashboard')


    context = {
        "event":event_obj,
        "form":form 
    }
    return render(request,'booking.html', context)

#As a user I can cancel a booking #(Not Working)for an event only 3 hours before the event.
def BookCancel(request,book_id):
    booking = Booking.objects.get(id=book_id)
    event =  Event.objects.get(id=booking.event.id)
    """ if event.start.hour - now.hour < 3:
        redirect('dashboard')"""
    event.limit += booking.tickets
    event.save()
    booking.delete()
  
    return redirect('dashboard')


def Profile(request):
    context = {
        "msg": 'hi!',
    }
    return render(request, 'profile.html', context)
 