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




]
