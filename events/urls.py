from django.urls import path,include
from django.contrib import admin
from events import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('api/',include('api.urls')),

	path('', views.home, name='home'),
	path('noaccess/', views.NoAccess, name='no-access'),

	path('dashboard/', views.Dashboard, name='dashboard'),
	path('profile/', views.Profile, name='profile'),

    path('dashboard/create/', views.EventCreate, name='create-event'),
    path('dashboard/<int:event_id>/update', views.EventUpdate, name='event-update'),
    

	path('events/', views.UpcomingEvents, name='events-list'),
	path('dashboard/<int:event_id>/', views.EventDetail, name='event-detail'),
	path('dashboard/<int:event_id>/book', views.EventBooking, name='event-booking'),
    path('dashboard/<int:book_id>/cancel', views.BookCancel, name='book-cancel'),
   
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
