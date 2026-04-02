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





















from django.utils.html import format_html

@admin.register(CustomTripInquiry)
class TripInquiryAdmin(BaseAdmin):

    list_display = [
        'full_name_display', 'destination', 'traveler_type',
        'travelers_count', 'duration_days', 'travel_date',
        'departure_airport', 'email', 'phone',
        'is_contacted', 'created_at',
    ]

    list_filter       = ['destination', 'traveler_type', 'duration_days', 'is_contacted']
    search_fields     = ['first_name', 'last_name', 'email', 'phone', 'destination']
    list_editable     = ['is_contacted']
    date_hierarchy    = 'created_at'
    readonly_fields   = ['created_at', 'daily_plan_display']

    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'notes')
        }),
        ('Trip Details', {
            'fields': (
                'traveler_type', 'travelers_count',
                'destination', 'duration_days',
                'departure_airport', 'travel_date',
            )
        }),
        ('Daily Itinerary Plan', {
            'fields': ('daily_plan_display',)
        }),
        ('Status', {
            'fields': ('is_contacted', 'created_at')
        }),
    )

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or '—'
    full_name_display.short_description = 'Name'

    def daily_plan_display(self, obj):
        if not obj.daily_plan:
            return '—'
        rows = ''.join(
            f"<tr>"
            f"<td style='padding:6px 12px; font-weight:600; white-space:nowrap; border-bottom:1px solid #eee;'>{day}</td>"
            f"<td style='padding:6px 12px; border-bottom:1px solid #eee;'>{', '.join(items) if items else '—'}</td>"
            f"</tr>"
            for day, items in obj.daily_plan.items()
        )
        return format_html(
            "<table style='border-collapse:collapse; min-width:400px;'>"
            "<thead><tr>"
            "<th style='padding:6px 12px; text-align:left; background:#f5f5f5; border-bottom:2px solid #ddd;'>Day</th>"
            "<th style='padding:6px 12px; text-align:left; background:#f5f5f5; border-bottom:2px solid #ddd;'>Itinerary Points</th>"
            "</tr></thead>"
            "<tbody>{}</tbody>"
            "</table>",
            format_html(rows)
        )
    daily_plan_display.short_description = 'Daily Plan'



















class PackageImageInline(TabularInline):
    model = PackageImage
    extra = 1


class PackageHighlightInline(StackedInline):
    model = PackageHighlight
    extra = 1


class InclusionInline(TabularInline):
    model = Inclusion
    extra = 1


class PackageActivityInline(StackedInline):
    model = PackageActivity
    extra = 1


@admin.register(TourDay)
class TourDayAdmin(BaseAdmin):
    list_display = ('name',)
@admin.register(Package)
class PackageAdmin(BaseAdmin):
    list_display = ('title', 'destination', 'tour_days', 'price', 'max_people')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        PackageImageInline,
        PackageHighlightInline,
        InclusionInline,
        PackageActivityInline
    ]





@admin.register(Lead)
class LeadAdmin(BaseAdmin):
    list_display = ('name','phone', 'created_at')
   