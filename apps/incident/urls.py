from django.urls import path
from apps.incident.views import (
    IncidentListView,
    IncidentDetailView,
    IncidentCreateView,
    IncidentUpdateView,
    IncidentDeleteView,
)


urlpatterns = [
    path(
        '',
        IncidentListView.as_view(),
        name='incident_home'
    ),
    path(
        '<int:pk>/',
        IncidentDetailView.as_view(),
        name='incident_detail'
    ),
    path(
        'new/',
        IncidentCreateView.as_view(),
        name='incident_create'
    ),
    path(
        '<int:pk>/update/',
        IncidentUpdateView.as_view(),
        name='incident_update'
    ),
    path(
        '<int:pk>/delete/',
        IncidentDeleteView.as_view(),
        name='incident_delete'
    ),
]
