from django.db import models

import django_filters
from django import forms
from django.db.models import Q

from apps.user.models import User

class UserFilter(django_filters.FilterSet):
    '''Filter rows from users list.'''

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'is_active', 'name', 'gender', 'age', 'occupation', 'village', 'taluka', 'district', 'state', 'pin_code', 'mobile_number_1', 'mobile_number_2']
        filter_overrides = {
            models.CharField: {
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
        }


    user_search = django_filters.CharFilter(method='user_search_filter')

    def user_search_filter(self, queryset, name, value):

        # check if search string is integer
        search_number = 999
        if value.isdigit():
            search_number = int(value)

        # add filtering on the role choice field
        choice_list = []
        choice_list.append(100)
        for role_choice in User.ROLE_CHOICES:
            choice = role_choice[1]
            if value.lower() in choice.lower():
                choice_list.append(role_choice[0])

        # add filtering on the gender choice field
        gender_list = []
        gender_list.append(100)
        for gender_choice in User.GENDER_CHOICES:
            choice = gender_choice[1]
            if value.lower() in choice.lower():
                gender_list.append(gender_choice[0])

        # add filtering on the occupation choice field
        occupation_list = []
        occupation_list.append(100)
        for occupation_choice in User.OCCUPATION_CHOICES:
            choice = occupation_choice[1]
            if value.lower() in choice.lower():
                occupation_list.append(occupation_choice[0])


        return User.objects.filter(
                Q(username__icontains=value) |
                Q(name__icontains=value) |
                Q(role__in=choice_list) |
                Q(gender__in=gender_list) |
                Q(age=search_number) |
                Q(occupation__in=occupation_list) |
                Q(village__icontains=value) |
                Q(taluka__icontains=value) |
                Q(district__icontains=value) |
                Q(state__icontains=value) |
                Q(pin_code=search_number) |
                Q(mobile_number_1__icontains=value) |
                Q(mobile_number_2__icontains=value) |
                Q(id=search_number)
            )
