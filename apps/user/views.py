
from collections import defaultdict
import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models import Count

from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)

from apps.incident.models import Incident
from apps.user.models import User
from apps.user.authorizations import Access
from apps.user.tables import UserTable
from apps.user.filters import UserFilter
from apps.user.forms import (
    UserCreationForm,
    UserChangeForm,
    UserUpdatePasswordForm,
)

# Dashboard functions to get summary, stats etc.
def get_user_count_total():
    return User.objects.all().count()


def get_new_user_count_this_month():
    # Users created in this calendar month
    first_day_of_the_current_month = datetime.datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
        )
    new_user_count = User.objects.filter(
        date_joined__gte=first_day_of_the_current_month
        ).count()
    return new_user_count


def get_incident_count_total():
    return Incident.objects.all().count()


def get_incident_count_emergency():
    return Incident.objects.filter(type=Incident.EMERGENCY).count()


def get_top_watchers_by_incident_count():
    # Top 5 watchers (by incident reports count)
    top_watchers = Incident.objects \
        .values('noter_id') \
        .annotate(count=Count('noter_id')) \
        .order_by('-count')[:5]
    for watcher in top_watchers:
        id = watcher['noter_id']
        noter = User.objects.get(id=id)
        watcher['noter_name'] = noter.name
    return top_watchers


def get_incident_count_by_type():
    # Top 5 types of incidents (by count)
    top_incident_types = Incident.objects \
        .values('type') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    # Incident type wise count
    type_choices = Incident.TYPE_CHOICES
    for incident_type in top_incident_types:
        type_number = incident_type['type']
        type_value = [v[1] for i, v in enumerate(type_choices) if v[0] == type_number][0]
        incident_type['type_value'] = type_value
    return top_incident_types


def get_incident_count_by_species():
    # Species wise count
    animal_list = defaultdict(int)
    species = Incident.objects.values_list('animal', flat=True)
    for animals in species:
        for animal in animals:
            animal_list[animal] += 1
    # animal_list =  sorted(animal_list)
    animal_list = dict(animal_list)
    animal_list = {
        k: v for k, v in sorted(animal_list.items(),
            key=lambda item: item[1],
            reverse=True
            )
        }
    return animal_list


# Create your views here.
@login_required
def watcher_home(request):
    '''Watcher home page. '''

    # watcher home page is accessible only to watcher role.
    role = request.user.role
    if 3 == role:
        return redirect(coordinator_home)
    if 4 == role:
        return redirect(manager_home)

    watcher_note_count = Incident.objects.filter(noter=request.user.id).count()

    context = {
     'watcher_note_count': watcher_note_count,
    }
    return render(request, 'user/watcher_home.html', context)


@login_required
def coordinator_home(request):
    '''Coordinator home page. '''

    # Coordinator home page is only accessible to coordinator role
    role = request.user.role
    if 2 == role:
        return redirect(watcher_home)
    if 4 == role:
        return redirect(manager_home)

    # # User counts
    # user_count_total = User.objects.all().count()
    # # Users created in this calendar month
    # first_day_of_the_current_month = datetime.datetime.now().replace(
    #     day=1, hour=0, minute=0, second=0, microsecond=0
    #     )
    # user_count_new_this_month = User.objects.filter(
    #     date_joined__gte=first_day_of_the_current_month
    #     ).count()

    # # Incident counts
    # incident_count_total = Incident.objects.all().count()
    # incident_count_emergency = Incident.objects.filter(type=Incident.EMERGENCY).count()

    # # Top 5 watchers (by incident reports count)
    # top_watchers = Incident.objects \
    #     .values('noter_id') \
    #     .annotate(count=Count('noter_id')) \
    #     .order_by('-count')[:5]
    # for watcher in top_watchers:
    #     id = watcher['noter_id']
    #     noter = User.objects.get(id=id)
    #     watcher['noter_name'] = noter.name

    # # Top 5 types of incidents (by count)
    # top_incident_types = Incident.objects \
    #     .values('type') \
    #     .annotate(count=Count('id')) \
    #     .order_by('-count')[:5]

    # # Incident type wise count
    # type_choices = Incident.TYPE_CHOICES
    # for incident_type in top_incident_types:
    #     type_number = incident_type['type']
    #     type_value = [v[1] for i, v in enumerate(type_choices) if v[0] == type_number][0]
    #     incident_type['type_value'] = type_value

    # # Species wise count
    # animal_list = defaultdict(int)
    # species = Incident.objects.values_list('animal', flat=True)
    # for animals in species:
    #     for animal in animals:
    #         animal_list[animal] += 1
    # # animal_list =  sorted(animal_list)
    # animal_list = dict(animal_list)
    # animal_list = {
    #     k: v for k, v in sorted(animal_list.items(),
    #         key=lambda item: item[1],
    #         reverse=True
    #         )
    #     }
    user_count_total = get_user_count_total()
    user_count_new_this_month = get_new_user_count_this_month()
    incident_count_total = get_incident_count_total()
    incident_count_emergency = get_incident_count_emergency()
    top_watchers = get_top_watchers_by_incident_count()
    top_incident_types = get_incident_count_by_type()
    animal_list = get_incident_count_by_species()

    context = {
        'user_count_total': user_count_total,
        'user_count_new_this_month': user_count_new_this_month,
        'incident_count_total': incident_count_total,
        'incident_count_emergency': incident_count_emergency,
        'top_watcher_by_report_count': top_watchers,
        'top_incident_type_by_report_count': top_incident_types,
        'species_by_report_count': animal_list,
    }
    return render(request, 'user/coordinator_home.html', context)


@login_required
def manager_home(request):
    '''Manager home page. '''

    # Manager dashboard is only accessible to manager role.
    role = request.user.role
    if 2 == role:
        return redirect(watcher_home)
    if 3 == role:
        return redirect(coordinator_home)

    user_count_total = get_user_count_total()
    user_count_new_this_month = get_new_user_count_this_month()
    incident_count_total = get_incident_count_total()
    incident_count_emergency = get_incident_count_emergency()
    top_watchers = get_top_watchers_by_incident_count()
    top_incident_types = get_incident_count_by_type()
    animal_list = get_incident_count_by_species()

    context = {
        'user_count_total': user_count_total,
        'user_count_new_this_month': user_count_new_this_month,
        'incident_count_total': incident_count_total,
        'incident_count_emergency': incident_count_emergency,
        'top_watcher_by_report_count': top_watchers,
        'top_incident_type_by_report_count': top_incident_types,
        'species_by_report_count': animal_list,
    }
    return render(request, 'user/manager_home.html', context)


class UserListView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        SingleTableMixin,
        ExportMixin,
        FilterView,
        ListView):
    model = User
    context_object_name = 'users'
    table_class = UserTable
    paginate_by = 15
    filterset_class = UserFilter
    template_name = 'user/dataset_01_user_list.html'

    def get_queryset(self):
        return User.objects.filter().order_by('id')

    def test_func(self):
        return Access.can_access_user_list(self)


class UserDetailView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        DetailView):
    model = User
    context_object_name = 'person'
    template_name = 'user/dataset_01_user_detail.html'

    def test_func(self):
        return Access.can_access_user_detail(self, self.get_object().id)


class UserCreateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        CreateView):
    model = User
    # fields = ['username', 'password', 'role', 'is_active']
    # context_object_name = 'person'
    form_class = UserCreationForm
    template_name = 'user/dataset_01_user_create.html'

    def test_func(self):
        return Access.can_create_user(self)


class UserUpdateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView):
    model = User
    # fields = ['username', 'password', 'role', 'is_active']
    context_object_name = 'person'
    form_class = UserChangeForm
    template_name = 'user/dataset_01_user_update.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        """

        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        return Access.can_update_user(self, self.get_object().id)


class UserUpdatePasswordView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView):
    model = User
    # fields = ['username', 'password', 'role', 'is_active']
    context_object_name = 'person'
    form_class = UserUpdatePasswordForm
    template_name = 'user/dataset_01_user_update_password.html'

    def form_valid(self, form):
        self.object = form.save()
        if 'password' in form.cleaned_data:
            if form.cleaned_data['password']:
                user_password = form.cleaned_data['password']
                print(user_password)
                self.object.set_password(user_password)
        return super().form_valid(form)

    def test_func(self):
        return Access.can_update_user(self, self.get_object().id)


class UserDeleteView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        DeleteView):
    model = User
    context_object_name = 'person'
    template_name = 'user/dataset_01_user_delete.html'
    success_url = '/user/'

    def test_func(self):
        return Access.can_delete_user(self)

