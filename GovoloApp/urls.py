from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index,name="index"),
   path('contact/',views.contact,name="contact"),
   path('blog/',views.blog,name="blog"),
   path('blogdetails/<slug:slug>',views.blog_detail,name="blogdetails"),

   path('about/',views.about,name="about"),

   path('destinations/',views.destinations,name="destinations"),
   path('destinations/<slug:slug>/',views.destination_detail,name="destination_detail"),

   path('api/destination-itineraries/', views.get_destination_itineraries, name='destination_itineraries'),

   path('api/submit-trip/', views.submit_trip_inquiry, name='submit_trip'), 


   path('packages/',views.packages,name="packages"),
   path('package/<slug:slug>/', views.package_detail, name='package_detail'),



   path('submit-lead/', views.submit_lead, name='submit_lead'),






]
