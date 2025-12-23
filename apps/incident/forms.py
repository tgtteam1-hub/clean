from django import forms
from apps.incident.models import Incident

import datetime

class IncidentCreateForm(forms.ModelForm):

    class Meta:
        model = Incident
        fields = (
            'geolocation',
            'information_type', 'type', 'date', 'timeslot',  'animal', 'animal_count',
            'location', 'village', 'taluka',
            'picture_1', 'picture_2', 'picture_3', 'picture_4',
            'description')
        exclude = ['noter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(datetime.date.today())
        # self.fields['date'].initial = '01-15-2023'
        # print(self.fields['date'])

    animal = forms.MultipleChoiceField(
        choices=Incident.ANIMAL_CHOICES,
        label='प्राणी'
        )
    today = datetime.date.today()
    date = forms.DateField(
        label="तारीख",
        required=True,
        initial=today,
        widget=forms.DateInput(
        #     format="%m-%d-%Y",
            attrs={"type": "date"}
        )
        # input_formats=["%m-%d-%Y"]
    )


class IncidentUpdateForm(forms.ModelForm):

    class Meta:
        model = Incident
        fields = (
            'geolocation',
            'information_type', 'type', 'date', 'timeslot', 'animal', 'animal_count',
            'location', 'village', 'taluka',
            'picture_1', 'picture_2', 'picture_3', 'picture_4',
            'description',
            'approval', 'reject_reason',
            'coordinator_note'
            )
        exclude = ['noter']

    def __init__(self, *args, **kwargs):
        request_present = False
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
            request_present = True
        super(IncidentUpdateForm, self).__init__(*args, **kwargs)
        # IF not user is NOT Coordinator, remove fields from form.
        if request_present:
             if not ( 3 == self.request.user.role ):
                 self.fields.pop('approval')
                 self.fields.pop('reject_reason')
                 self.fields.pop('coordinator_note')

    animal = forms.MultipleChoiceField(
        choices=Incident.ANIMAL_CHOICES,
        label='प्राणी'
        )
    date = forms.DateField(
        label="तारीख",
        required=True,
        widget=forms.DateInput(
            # format="%m-%d-%Y",
            attrs={"type": "date"}
        )
    )
