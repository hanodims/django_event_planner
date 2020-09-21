from django.urls import path
from django.contrib import admin
from events import views

urlpatterns = [

	path('', views.home, name='home'),
	path('noaccess/', views.NoAccess, name='no-access'),

	path('dashboard/', views.Dashboard, name='dashboard'),
	path('dashboard/<int:event_id>/', views.EventDetail, name='event-detail'),
	path('dashboard/create/', views.EventCreate, name='create-event'),
	path('dashboard/<int:event_id>/update', views.EventUpdate, name='event-update'),
	path('events/', views.UpcomingEvents, name='events-list'),
	path('dashboard/<int:event_id>/book', views.EventBooking, name='event-booking'),
   
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]

