# from django.utils.html import format_html

import django_tables2 as tables
from django_tables2.utils import A # Alias for Accessor

from apps.incident.models import Incident


class IncidentTable(tables.Table):

    class Meta:
        model = Incident
        exclude = ('noter', 'title')
        extra_columns = ('noter__name')
        sequence = (
            'id', 'information_type',
            'type', 'date', 'timeslot', 'animal', 'animal_count',
            'location', 'village', 'taluka',
            'description',
            'noter__name', 'approval',  'reject_reason',
            'coordinator_note',
        )
        order_by = '-id'
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {
            'id' : 'activity_table_01',
            'class' : 'table table-striped',
            'thead' : {'class': 'thead-dark'}
        }

    # def render_noter__name(self, value, record):
    #     detail_url = reverse('user_detail', kwargs={'pk': record.noter.pk})
    #     return format_html('<a href="{}">{}</a>', detail_url, value)

    # def render_date(self, value, record):
    #     return format_html('<span style="font-size:0.8em;">{}</span>', value)

    id = tables.LinkColumn(
        'incident_detail',
        args=[A('pk')],
    )
    # title = tables.LinkColumn(
    #     'incident_detail',
    #     args=[A('pk')],
    #     visible=False,
    # )
    date = tables.DateColumn(
        format ='d-M-Y',
    )
    animal = tables.Column(
        accessor='get_animal_list',
        verbose_name='प्राणी'
        )
    description = tables.Column(
        visible=False,
    )
    picture_1 = tables.Column(
        visible=False,
    )
    picture_2 = tables.Column(
        visible=False,
    )
    picture_3 = tables.Column(
        visible=False,
    )
    picture_4 = tables.Column(
        visible=False,
    )
    noter__name = tables.LinkColumn(
        'user_detail',
        args=[A('noter.id')],
        verbose_name='नोंद करणारी व्यक्ती',
        )
    approval = tables.Column(
        verbose_name='मान्यता'
     )
    reject_reason = tables.Column(
        visible=False,
        verbose_name='नाकारण्याचे कारण'
    )
    coordinator_note = tables.Column(
        visible=False,
    )
