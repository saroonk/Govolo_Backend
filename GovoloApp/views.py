import threading
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import *

from django.core.paginator import Paginator
# Create your views here.



def send_contact_email(data):
    subject = "New Travel Inquiry"

    message = f"""
    Name: {data['full_name']}
    Email: {data['email']}
    Phone: {data['phone']}
    Travel Date: {data['travel_date']}
    Trip Type: {data['trip_type']}
    Budget: {data['budget']}
    Message: {data['message']}
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )



def index(request):
    gallery = GalleryImages.objects.all()
    testi = Testimonial.objects.all().order_by('-rating')
    hero = HeroSection.objects.first()
    tour_category =TourCategory.objects.all().order_by('-id')
    top_destinations = Destination.objects.filter(is_top=True,is_active=True).order_by('-id')[:7]
    all_destinations = Destination.objects.filter(is_active=True).order_by('-id')

    destination_types = DestinationType.objects.prefetch_related(
        'regions__destinations'
    )
    context = {'gallery':gallery,'testimonial':testi,'hero': hero,'tour_category': tour_category,'top_destinations': top_destinations,'all_destinations': all_destinations}
    return render(request,"index.html",context)






def contact(request):
    if request.method == "POST":

        data = {
            'full_name': request.POST.get('fullName'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'travel_date': request.POST.get('travelDate'),
            'trip_type': request.POST.get('tripType'),
            'budget': request.POST.get('budget'),
            'message': request.POST.get('message'),
        }

       
        Contact.objects.create(**data)

        print("_____________________________created")

        threading.Thread(target=send_contact_email, args=(data,)).start()

        messages.success(request, "Message sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html')





def blog(request):
    blogs = Blog.objects.select_related('category').order_by('-created_at')
    categories = BlogCategory.objects.all()

    paginator =Paginator(blogs,20)
    page_number = request.GET.get('page')
    page_obj =paginator.get_page(page_number)


    context = {
        'blogs': page_obj,
        'categories': categories,
        'page_obj': page_obj
    }

    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    recent = Blog.objects.all().order_by('-created_at').exclude(slug=slug)
    return render(request, 'blog-detail.html', {'blog': blog,"recent":recent})


def about(request):
    return render(request,'aboutus.html')

def destinations(request):
    destination = Destination.objects.filter(is_active=True).order_by('-id')

    return render(request,'destination-listing.html',{'destinations':destination})


def destination_detail(request,slug):
    destination = Destination.objects.prefetch_related('images','highlights').get(slug=slug)
    testi = Testimonial.objects.all().order_by('-rating')

    return render(request,'destinationdetail.html',{'destination':destination,'testimonial':testi})