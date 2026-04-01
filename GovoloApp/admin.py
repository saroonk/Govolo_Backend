from django.contrib import admin
from unfold.admin import StackedInline

try:
    from unfold.admin import ModelAdmin as BaseAdmin
except Exception:
    from django.contrib.admin import ModelAdmin as BaseAdmin

from .models import *

from django.http import HttpResponse

from unfold.admin import ModelAdmin

from unfold.admin import StackedInline, TabularInline
from unfold.forms import AdminPasswordChangeForm , UserChangeForm , UserCreationForm
from django.contrib.admin import register
from django.contrib.auth.models import User





class HeroMediaInline(TabularInline):
    model = HeroMedia
    extra = 1


# ✅ Main admin
@admin.register(HeroSection)
class HeroSectionAdmin(BaseAdmin):
    inlines = [HeroMediaInline]

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request) 


@admin.register(GalleryImages)
class GalleryAdmin(BaseAdmin):
    list_display = ('image',)




@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = ("name", "designation", "rating","created_at")
    list_filter = ("rating",)
    search_fields = ("name", "designation")




@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'trip_type',
        'budget',
        'travel_date',
        'created_at'
    )

    list_filter = (
        'trip_type',
        'budget',
        'travel_date',
        'created_at'
    )

    search_fields = (
        'full_name',
        'email',
        'phone'
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)









@admin.register(BlogCategory)
class BlogCategoryAdmin(BaseAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'author')
    ordering = ('-created_at',)

    prepopulated_fields = {"slug": ("title",)}










@admin.register(TourCategory)
class TourCategoryAdmin(BaseAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}








# ==========================================
# Inline Models
# ==========================================
class DestinationImageInline(TabularInline):
    model = DestinationImage
    extra = 1


class DestinationHighlightInline(TabularInline):
    model = DestinationHighlight
    extra = 1


class DestinationItineraryInline(StackedInline):
    model = DestinationItinerary
    extra = 1


# ==========================================
# Destination Admin
# ==========================================
@admin.register(Destination)
class DestinationAdmin(BaseAdmin):
    list_display = ('title', 'region', 'is_active', 'is_top', 'show_in_navbar')
    list_filter = ('region', 'is_active', 'is_top', 'show_in_navbar')
    search_fields = ('title', 'subtitle')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        DestinationImageInline,
        DestinationHighlightInline,
        DestinationItineraryInline,
    ]


# ==========================================
# Destination Type Admin
# ==========================================
@admin.register(DestinationType)
class DestinationTypeAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ==========================================
# Destination Region Admin
# ==========================================
@admin.register(DestinationRegion)
class DestinationRegionAdmin(BaseAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)