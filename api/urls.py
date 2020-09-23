from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('apilogin/', views.UserLoginAPIView.as_view(), name='api-login'),
    path('register/', views.UserCreateAPIView.as_view(), name="register"),


    path('', views.UpcomingEventsList.as_view(), name="api-upcoming-events-list"),
    path('<int:event_id>/', views.EventDetail.as_view(), name="api-event-detail"),
    path('create/', views.EventCreate.as_view(), name="api-create-event"),
    path('<int:event_id>/update/', views.EventUpdate.as_view(), name="api-update-event"),
    path('<int:event_id>/bookers/', views.Bookers.as_view(), name="api-event-bookers"),
    path('<int:event_id>/booking/', views.BookingEvent.as_view(), name="api-event-bookers"),


    path('myevents/', views.MyEventsList.as_view(), name="api-my-events"),
    path('mybookings/', views.MyBookingList.as_view(), name="api-my-bookings"),
    

]
