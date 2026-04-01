from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
# Create your models here.




class HeroSection(models.Model):
    subtitle = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)

    btn1_text = models.CharField(max_length=100, blank=True)
    btn2_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


# ✅ Multiple media (slider items)
class HeroMedia(models.Model):
    hero = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name='media_items'
    )

    media_file = models.FileField(
        upload_to='hero/',
       
    )

    order = models.PositiveIntegerField(default=0)  # for sorting

    def __str__(self):
        return f"{self.hero.title} - Media {self.id}"

    class Meta:
        ordering = ['order']


class GalleryImages(models.Model):
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"


class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class Contact(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    travel_date = models.DateField()
    trip_type = models.CharField(max_length=50)
    budget = models.CharField(max_length=50)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name






class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name="blogs"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.CharField(
        max_length=300,
        help_text="This will show on blog cards"
    )

    main_image = models.ImageField(upload_to='blogs/')

    content = RichTextField()

    author = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title





class TourCategory(models.Model):
    name = models.CharField(max_length=200, help_text="e.g. Solo, Family, Group Tours, etc.")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='tour_categories/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name















# ==========================================
# Destination Type (International / Domestic)
# ==========================================
class DestinationType(models.Model):
    name = models.CharField(max_length=100,help_text="e.g. International, Domestic")

    def __str__(self):
        return self.name


# ==========================================
# Continent / Region (Asia, Europe, etc.)
# ==========================================
class DestinationRegion(models.Model):
    type = models.ForeignKey(
        DestinationType,
        on_delete=models.CASCADE,
        related_name='regions'
    )
    name = models.CharField(max_length=100, help_text="e.g. Asia, Europe, etc.")

    def __str__(self):
        return f"{self.type.name} - {self.name}"


# ==========================================
# Main Destination
# ==========================================
class Destination(models.Model):
    region = models.ForeignKey(
        DestinationRegion,
        on_delete=models.CASCADE,
        related_name='destinations'
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    subtitle = models.CharField(max_length=255, blank=True)
    description = RichTextField()

    main_image = models.ImageField(upload_to='destinations/')
    video = models.FileField(upload_to='destinations/videos/', blank=True, null=True,help_text="This video will be used in the destination detail hero section")
    badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. used in navbar, highlights, etc.")
    
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False) 
    show_in_navbar = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# ==========================================
# Multiple Images
# ==========================================
class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='destination_gallery/')


    def __str__(self):
        return self.destination.title


# ==========================================
# Highlights
# ==========================================
class DestinationHighlight(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='highlights'
    )

    title = models.CharField(max_length=200)
    icon = models.CharField(
        max_length=100,
        blank=True,
        default="fa-solid fa-star" 
    )

    def __str__(self):
        return self.title


# ==========================================
# Itinerary Points
# ==========================================
class DestinationItinerary(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='itineraries'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.title