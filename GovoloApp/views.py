import threading
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from django.db.models import Q

from django.core.paginator import Paginator
# Create your views here.

from django.http import JsonResponse

import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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






def send_new_lead_email(inquiry):
    """
    Builds and sends a notification email for a new CustomTripInquiry.
    Called in a background thread so it never delays the HTTP response.
    """

    daily_plan_lines = []
    for day, points in inquiry.daily_plan.items():
        points_str = ', '.join(points) if points else 'No points selected'
        daily_plan_lines.append(f"  {day}: {points_str}")
    daily_plan_text = '\n'.join(daily_plan_lines) or '  Not specified'

    subject = f"New Custom Trip Inquiry — {inquiry.destination} ({inquiry.traveler_type})"

    message = f"""
A new custom trip inquiry has been submitted.

─────────────────────────────
TRAVELER DETAILS
─────────────────────────────
Name        : {inquiry.first_name} {inquiry.last_name}
Email       : {inquiry.email}
Phone       : {inquiry.phone}

─────────────────────────────
TRIP DETAILS
─────────────────────────────
Destination : {inquiry.destination}
Traveler    : {inquiry.traveler_type} ({inquiry.travelers_count} traveler(s))
Duration    : {inquiry.duration_days} Days
Departure   : {inquiry.departure_airport}
Start Date  : {inquiry.travel_date}

─────────────────────────────
DAILY ITINERARY PLAN
─────────────────────────────
{daily_plan_text}

─────────────────────────────
ADDITIONAL NOTES
─────────────────────────────
{inquiry.notes or 'None'}

─────────────────────────────
Submitted at: {inquiry.created_at.strftime('%d %B %Y, %I:%M %p')}
    """.strip()

    send_mail(
        subject      = subject,
        message      = message,
        from_email   = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [settings.DEFAULT_FROM_EMAIL],
        fail_silently = True,   # won't crash the app if email fails
    )




def index(request):
    gallery = GalleryImages.objects.all()
    testi = Testimonial.objects.all().order_by('-rating')
    hero = HeroSection.objects.first()
    tour_category =TourCategory.objects.all().order_by('-id')
    top_destinations = Destination.objects.filter(is_top=True,is_active=True).order_by('-id')[:7]
    all_destinations = Destination.objects.filter(is_active=True).order_by('title')
    recent_packages = Package.objects.select_related('destination').filter(is_active=True).order_by('-id')[:3]

    destination_types = DestinationType.objects.prefetch_related(
        'regions__destinations'
    )
    context = {'gallery':gallery,'testimonial':testi,'hero': hero,'tour_category': tour_category,'top_destinations': top_destinations,'all_destinations': all_destinations,'recent_packages': recent_packages}
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
    destination = Destination.objects.prefetch_related('images','highlights', 'packages__tour_days', 'packages__tour_category').get(slug=slug)
    testi = Testimonial.objects.all().order_by('-rating')
    all_destinations = Destination.objects.filter(is_active=True).order_by('title')

    # Couple
    couple_packages = destination.packages.filter(is_active=True, tour_category__slug='couple').order_by('-id')[:8]
    couple_durations = sorted(set(p.tour_days for p in couple_packages if p.tour_days), key=lambda x: str(x.name))

    # Family
    family_packages = destination.packages.filter(is_active=True, tour_category__slug='family').order_by('-id')[:8]
    family_durations = sorted(set(p.tour_days for p in family_packages if p.tour_days), key=lambda x: str(x.name))

    # Solo
    solo_packages = destination.packages.filter(is_active=True, tour_category__slug='solo').order_by('-id')[:8]
    solo_durations = sorted(set(p.tour_days for p in solo_packages if p.tour_days), key=lambda x: str(x.name))

    context = {
        'destination': destination,
        'testimonial': testi,
        'couple_packages': couple_packages,
        'couple_durations': couple_durations,
        'family_packages': family_packages,
        'family_durations': family_durations,
        'solo_packages': solo_packages,
        'solo_durations': solo_durations,
        'all_destinations': all_destinations,
    }

    return render(request,'destinationdetail.html', context)


def destination_type_list(request, slug):

    type = DestinationType.objects.get(slug=slug)

    destinations = Destination.objects.filter(
        type__slug=slug,
        is_active=True
    ).select_related('region').order_by('-id')


    return render(request, 'destination-listing.html', {
        'destinations': destinations,
        'type': type,
      
    })

def get_destination_itineraries(request):
    destination_slug = request.GET.get('slug', '').strip()
    if not destination_slug:
        return JsonResponse({'itineraries': []}, status=400)

    try:
        dest = Destination.objects.get(slug=destination_slug)
        itineraries = list(
            dest.itineraries.values('id', 'title', 'description')
        )
        return JsonResponse({'itineraries': itineraries})
    except Destination.DoesNotExist:
        return JsonResponse({'itineraries': []}, status=404)















def custom_trip_email_center(inquiry):
    """
    Spawns a background thread to send the lead notification email.
    This keeps the HTTP response fast — email sending never blocks it.
    """
    thread = threading.Thread(
        target=send_new_lead_email,
        args=(inquiry,),
        daemon=True   # thread dies automatically if the server shuts down
    )
    thread.start()








@csrf_exempt
@require_POST
def submit_trip_inquiry(request):
    try:
        body = json.loads(request.body)

        duration_days = int(body.get('duration_days', 5))
        daily_plan = {}
        for i in range(1, duration_days + 1):
            raw = body.get(f'day_{i}_cities', '')
            daily_plan[f'Day {i}'] = [c.strip() for c in raw.split(',') if c.strip()]

        inquiry = CustomTripInquiry.objects.create(
            traveler_type     = body.get('traveler_type', ''),
            travelers_count   = int(body.get('travelers', 1) or 1),
            destination       = body.get('destination', ''),
            duration_days     = duration_days,
            departure_airport = body.get('departure_airport', ''),
            travel_date       = body.get('travel_date') or None,
            daily_plan        = daily_plan,
            first_name        = body.get('first_name', ''),
            last_name         = body.get('last_name', ''),
            email             = body.get('email', ''),
            phone             = body.get('phone', ''),
            notes             = body.get('notes', ''),
        )

        # Fire and forget — response returns immediately, email sends in background
        custom_trip_email_center(inquiry)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)




def packages(request):
    destinations = Destination.objects.filter(is_active=True).order_by('title')
    tour_categories = TourCategory.objects.all().order_by('name')

    selected_dest = request.GET.get('destination', '')
    selected_tour_type = request.GET.get('tour_type', '')
    selected_duration = request.GET.get('duration', '')
    selected_price = request.GET.get('price', '')
    selected_sort = request.GET.get('sort', 'newest')

    packages_query = Package.objects.select_related('destination','tour_days','tour_category').filter(is_active=True)

    if selected_dest:
        packages_query = packages_query.filter(destination__slug=selected_dest)
    
    if selected_tour_type:
        packages_query = packages_query.filter(tour_category__slug=selected_tour_type)

    if selected_duration:
        packages_query = packages_query.filter(tour_days__name=selected_duration)

    if selected_price:
        if selected_price == "0-5000":
            packages_query = packages_query.filter(price__lte=5000)
        elif selected_price == "5000-10000":
            packages_query = packages_query.filter(price__gt=5000, price__lte=10000)
        elif selected_price == "10000-20000":
            packages_query = packages_query.filter(price__gt=10000, price__lte=20000)
        elif selected_price == "20000+":
            packages_query = packages_query.filter(price__gt=20000)

    if selected_sort == 'price-asc':
        packages_query = packages_query.order_by('price')
    elif selected_sort == 'price-desc':
        packages_query = packages_query.order_by('-price')
    elif selected_sort == 'oldest':
        packages_query = packages_query.order_by('id')
    else:  # newest
        packages_query = packages_query.order_by('-id')

    paginator = Paginator(packages_query, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'packages': page_obj, 
        'page_obj': page_obj,
        'destinations': destinations,
        'tour_categories': tour_categories,
        'selected_dest': selected_dest,
        'selected_tour_type': selected_tour_type,
        'selected_duration': selected_duration,
        'selected_price': selected_price,
        'selected_sort': selected_sort,
    }

    return render(request,'package-listingss.html', context)


def package_detail(request, slug):
    all_destinations = Destination.objects.filter(is_active=True).order_by('title')

    package = get_object_or_404(Package.objects.select_related('destination','tour_days').prefetch_related('highlights', 'images','inclusions','activities'), slug=slug)

    inclusions = list(package.inclusions.all())
    half = (len(inclusions) + 1) // 2  

    left_inclusions = inclusions[:half]
    right_inclusions = inclusions[half:]
    activities = package.activities.order_by('day')
    testi = Testimonial.objects.all().order_by('-rating')


    similar_packages = Package.objects.filter(Q(destination=package.destination) | Q(tour_category=package.tour_category)).exclude(id=package.id).order_by('-id')[:3]
    return render(request,'package-detail.html',{'lead_already_submitted': request.session.get('lead_submitted', False),'package':package, 'left_inclusions': left_inclusions, 'right_inclusions': right_inclusions, 'activities': activities, 'similar_packages': similar_packages,'testimonial':testi,'all_destinations': all_destinations})




@require_POST
def submit_lead(request):
    # Already submitted in this session → just unlock
    if request.session.get('lead_submitted'):
        return JsonResponse({'success': True})

    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()

    # Basic validation
    if not name:
        return JsonResponse({'success': False, 'errors': {'name': 'Name is required.'}})
    if not phone:
        return JsonResponse({'success': False, 'errors': {'phone': 'Phone number is required.'}})
    if not phone.isdigit() or len(phone) < 10:
        return JsonResponse({'success': False, 'errors': {'phone': 'Enter a valid phone number.'}})

    # Save to DB
    Lead.objects.create(name=name, phone=phone)

    # Mark session
    request.session['lead_submitted'] = True
    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

    return JsonResponse({'success': True})




def send_new_package_email(data):
    subject = "New Travel Package Inquiry"

    message = f"""
    Name: {data['full_name']}
    Phone: {data['phone']}
    Package: {data['package']}
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


@csrf_exempt
@require_POST
def submit_package_inquiry(request):
    try:
        body = json.loads(request.body)
        
        package_id = body.get('package_id')
        package = get_object_or_404(Package, id=package_id)

        inquiry = PackageInquiry.objects.create(
            package=package,
            full_name=body.get('full_name', ''),
            phone=body.get('phone', ''),
            travel_date=body.get('travel_date'),
            trip_type=body.get('trip_type', ''),
            budget=body.get('budget', ''),
            message=body.get('message', ''),
        )

        email_data = {
            "full_name": inquiry.full_name,
            "phone": inquiry.phone,
            "package": inquiry.package.title,
            "travel_date": inquiry.travel_date,
            "trip_type": inquiry.trip_type,
            "budget": inquiry.budget,
            "message": inquiry.message,
        }

        thread = threading.Thread(
            target=send_new_package_email,
            args=(email_data,),
            daemon=True   
        )
        thread.start()


        return JsonResponse({'success': True, 'message': 'Inquiry submitted successfully!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
