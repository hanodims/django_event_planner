from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),

    path('', views.UpcomingEventsList.as_view(), name="api-upcoming-events-list"),
    path('<int:event_id>/', views.EventDetail.as_view(), name="api-event-detail"),

    path('myevents/', views.MyEventsList.as_view(), name="api-my-events"),
]
