from django.db.models import Prefetch
from .models import DestinationType, Destination


def navbar_destinations(request):
    destination_types = DestinationType.objects.prefetch_related(
        Prefetch(
            'regions__destinations',
            queryset=Destination.objects.filter(
                show_in_navbar=True,
                is_active=True
            )
        )
    )

    return {
        'nav_destination_types': destination_types
    }







# from django.db.models import Prefetch
# from .models import DestinationType, Destination


# def navbar_destinations(request):
#     destination_types = DestinationType.objects.prefetch_related(
#         Prefetch(
#             'regions__destinations',
#             queryset=Destination.objects.filter(
#                 show_in_navbar=True,
#                 is_active=True
#             )
#         )
#     )

#     final_types = []

#     for t in destination_types:
#         regions = []
#         total_destinations = 0

#         for r in t.regions.all():
#             destinations = list(r.destinations.all())
#             if destinations:
#                 r.filtered_destinations = destinations
#                 regions.append(r)
#                 total_destinations += len(destinations)

#         t.filtered_regions = regions
#         t.total_destinations = total_destinations

#         final_types.append(t)

#     return {
#         'nav_destination_types': final_types
#     }