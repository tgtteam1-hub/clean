from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
import django_filters

from apps.incident.models import Incident


class IncidentFilter(django_filters.FilterSet):
    '''Filter rows from incident list.'''

    animal = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Incident
        fields = [ 'id', 'information_type', 'date', 'timeslot', 'type', 'animal', 'animal_count', 'location', 'village', 'taluka',
        'approval', 'noter__name', 'noter_id' #'animal_search',
        ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'style': 'max-width:100px;'})
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'style': 'max-width:100px;'})
                },
            },
            models.PositiveSmallIntegerField: {
                'filter_class': django_filters.NumberFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'style': 'max-width:50px;'})
                },
            },
            models.PositiveIntegerField: {
                'filter_class': django_filters.NumberFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'style': 'max-width:100px;'})
                },
            },
            models.IntegerField: {
                'filter_class': django_filters.NumberFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'style': 'max-width:50px;'})
                },
            },
             models.AutoField: {
                'filter_class': django_filters.NumberFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'style': 'max-width:50px;'})
                },
            },
            models.DateField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'style': 'max-width:100px;'})
                },
            },
        }

    # animal = django_filters.CharFilter(
    #     widget=forms.TextInput(attrs={'style': 'max-width:130px;'})
    # )

    animal = django_filters.CharFilter(
        method='animal_search_filter',
         widget=forms.TextInput(attrs={'style': 'max-width:130px;'})
         )
    def animal_search_filter(self, queryset, name, value):
        # if self.role in [1, 2]:
        #     return Incident.objects.filter(
        #         Q(animal__contains=[value]) &
        #         Q(noter__id=self.id)
        #         )
        # else:
        return Incident.objects.filter(animal__contains=[value])

    # animal_search = django_filters.CharFilter(method='animal_search_filter')
    # def animal_search_filter(self, queryset, name, value):
    #     animal_list = []
    #     for animal in Incident.ANIMAL_CHOICES:
    #         animal_name = animal[1]
    #         if value.lower() in animal_name.lower():
    #             animal_list.append(animal[0])
    #     print(animal_list)
    #     return Incident.objects.filter(
    #         Q(title__icontains=value)
    #         # Q(animal_1__in=animal_list) #|
    #         # Q(animal_2__in=animal_list) |
    #         # Q(animal_3__in=animal_list) |
    #         # Q(animal_4__in=animal_list)
    #     )

    activity_search = django_filters.CharFilter(method='incident_search_filter')
    def incident_search_filter(self, queryset, name, value):

        # check if search string is integer
        search_number = 999
        if value.isdigit():
            search_number = int(value)

        timeslot_list = []
        timeslot_list.append(100)
        for timeslot_choice in Incident.TIMESLOT_CHOICES:
            choice = timeslot_choice[1]
            if value.lower() in choice.lower():
                timeslot_list.append(type_choice[0])

        # add filtering on the type choice field
        type_list = []
        type_list.append(100)
        for type_choice in Incident.TYPE_CHOICES:
            choice = type_choice[1]
            if value.lower() in choice.lower():
                type_list.append(type_choice[0])

        # add filtering on the approval choice field
        approval_list = []
        approval_list.append(100)
        for approval_choice in Incident.APPROVAL_STATUS_CHOICES:
            choice = approval_choice[1]
            if value.lower() in choice.lower():
                approval_list.append(approval_choice[0])

        return Incident.objects.filter(
                #Q(title__icontains=value) |
                Q(noter__name__icontains=value) |
                Q(timeslot__in=timeslot_list) |
                Q(type__in=type_list) |
                Q(description__icontains=value) |
                Q(approval__in=approval_list) |
                Q(reject_reason__icontains=value) |
                Q(animal__contains=[value]) |
                Q(location__icontains=value) |
                Q(village__icontains=value) |
                Q(taluka__icontains=value) |
                # Q(animal_count=value |
                # Q(age=search_number) |
                # Q(pin_code=search_number) |
                # Q(mobile_number__icontains=value) |
                Q(id=search_number) |
                Q(coordinator_note__icontains=value)
            )
