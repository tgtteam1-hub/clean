from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

from apps.incident.models import Incident
from apps.incident.authorizations import Access
from apps.incident.tables import IncidentTable
from apps.incident.filters import IncidentFilter
from apps.incident.forms import IncidentCreateForm, IncidentUpdateForm
from apps.user.models import User


class IncidentListView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        SingleTableMixin,
        ExportMixin,
        FilterView,
        ListView):
    model = Incident
    context_object_name = 'activity'
    table_class = IncidentTable
    paginate_by = 10
    filterset_class = IncidentFilter
    template_name = 'incident/dataset_01_incident_list.html'

    def get_queryset(self):
        if self.request.user.role in [ User.COORDINATOR, User.MANAGER ] :
            return Incident.objects.filter().order_by('id')
        else:
            # Watcher can only view her incident list
            return Incident.objects.filter(noter=self.request.user).order_by('id')

    def test_func(self):
        return Access.can_access_incident_list(self)


class IncidentDetailView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        DetailView):
    model = Incident
    context_object_name = 'activity'
    template_name = 'incident/dataset_01_incident_detail.html'

    def test_func(self):
        return Access.can_access_incident_detail(self, self.get_object().noter.id)


class IncidentCreateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        CreateView):
    model = Incident
    form_class = IncidentCreateForm
    template_name = 'incident/dataset_01_incident_create.html'

    # Pre-populate village and taluka fields on incident create form
    def get_initial(self):
        initial = super().get_initial()
        initial['village'] = self.request.user.village
        initial['taluka'] = self.request.user.taluka
        return initial

    def form_valid(self, form):
        form.instance.noter = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return Access.can_create_incident(self)


class IncidentUpdateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView):
    model = Incident
    # fields = ['username', 'password', 'role', 'is_active']
    context_object_name = 'activity'
    form_class = IncidentUpdateForm
    template_name = 'incident/dataset_01_incident_update.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        """

        kwargs = super(IncidentUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        return Access.can_update_incident(
            self, self.get_object().noter.id, self.get_object().approval
        )


class IncidentDeleteView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        DeleteView):
    model = Incident
    context_object_name = 'activity'
    template_name = 'incident/dataset_01_incident_delete.html'
    success_url = '/incident/'

    def test_func(self):
        return Access.can_delete_incident(self, self.get_object().noter.id)

