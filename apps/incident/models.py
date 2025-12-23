from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

import datetime

from apps.user.models import User


class Incident(models.Model):
    ''' Stores Wildlife incident information reported by watchers and used for analysis.
    '''

    # Type of incident
    OTHER_TYPE = 1
    SIGHTING = 2
    EMERGENCY = 3
    HUNT_KILL = 4
    LIVESTOCK_KILL = 5
    SMUGGLE = 6
    TYPE_CHOICES = (
        (SIGHTING, 'सायटिंग'),
        (EMERGENCY, 'आपत्कालीन / इमर्जन्सी / जखमी प्राणी'),
        (HUNT_KILL, 'शिकार / मृत्यू'),
        (LIVESTOCK_KILL, 'पशुधन हत्या'),
        (SMUGGLE, 'तस्करी'),
        (OTHER_TYPE, 'इतर'),
    )

    # Approval status options
    OTHER_APPROVAL_STATUS = 1
    PENDING = 2
    APPROVED = 3
    REJECTED = 4
    APPROVAL_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )

    # Animal options
    OTHER_ANIMAL = 'इतर'
    ANIMAL1 = 'लांडगा'
    ANIMAL2 = 'तरस'
    ANIMAL3 = 'कोल्हा'
    ANIMAL4 = 'खोकड'
    ANIMAL5 = 'बिबट्या'
    ANIMAL6 = 'चिंकारा/हरीण'
    ANIMAL7 = 'काळवीट'
    ANIMAL8 = 'भटकी कुत्री'
    ANIMAL_CHOICES = (
        (ANIMAL1, 'लांडगा'),
        (ANIMAL2, 'पट्टेरी तरस'),
        (ANIMAL3, 'कोल्हा'),
        (ANIMAL4, 'खोकड'),
        (ANIMAL5, 'बिबट्या'),
        (ANIMAL6, 'चिंकारा/हरीण'),
        (ANIMAL7, 'काळवीट'),
        (ANIMAL8, 'भटकी कुत्री'),
        (OTHER_ANIMAL, 'इतर')
    )

    # Information type options
    HEARD = 1
    WATCHED = 2
    INFORMATION_TYPE_CHOICES = (
        (HEARD, 'ऐकलेले'),
        (WATCHED, 'पाहिलेले')
    )

    # Timeslot options
    UNKNOWN = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4
    TIMESLOT_CHOICES = (
        (UNKNOWN, 'माहिती नाही'),
        (MORNING, 'सकाळ'),
        (AFTERNOON, 'दुपार'),
        (EVENING, 'संध्याकाळ'),
        (NIGHT, 'रात्र'),
    )

    id = models.AutoField(
        primary_key=True,
        verbose_name=('ID')
    )
    title = models.CharField(
        max_length=50,
        default='-',
        verbose_name=('शीर्षक'),
    )
    information_type = models.PositiveSmallIntegerField(
        choices=INFORMATION_TYPE_CHOICES,
        default=2,
        verbose_name=('रिपोर्टींग')
    )
    date = models.DateField(
        default=datetime.date.today,
        verbose_name=('तारीख')
    )
    timeslot = models.PositiveSmallIntegerField(
        choices=TIMESLOT_CHOICES,
        default=0,
        verbose_name=('वेळ')
    )
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=2,
        verbose_name=('घटना प्रकार')
    )
    animal = ArrayField(
        models.CharField(
            choices=ANIMAL_CHOICES,
            default='इतर',
            verbose_name=('प्राणी')
        ),
        verbose_name='प्राणी',
        blank=True,
        null=True
    )
    animal_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=('प्राणी संख्या')
    )
    geolocation = models.CharField(
        default='NA',
        max_length=100,
        verbose_name=('नकाशा ठिकाण')
    )
    location = models.CharField(
        # default='-',
        max_length=100,
        verbose_name=('ठिकाण')
    )
    village = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('गाव'),
    )
    taluka = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('तालुका'),
    )
    description = models.TextField(
        default='-',
        verbose_name=('वर्णन/अधिक माहिती')
    )
    picture_1 = models.ImageField(
        # default = 'incident_pics/default_animal_1.png',
        upload_to = 'incident_pics',
        verbose_name=('फोटो १'),
        help_text='( किमान एक फोटो आवश्यक आहे )'
    )
    picture_2 = models.ImageField(
        default = 'incident_pics/default_animal_2.png',
        upload_to = 'incident_pics',
        verbose_name=('फोटो २'),
        blank=True
    )
    picture_3 = models.ImageField(
        default = 'incident_pics/default_animal_2.png',
        upload_to = 'incident_pics',
        verbose_name=('फोटो ३'),
        blank=True
    )
    picture_4 = models.ImageField(
        default = 'incident_pics/default_animal_2.png',
        upload_to = 'incident_pics',
        verbose_name=('फोटो ४'),
        blank=True
    )
    noter = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        default = 12,
        related_name = 'incident_noter',
    )
    approval = models.PositiveSmallIntegerField(
        choices=APPROVAL_STATUS_CHOICES,
        default=2,
        verbose_name=('नोंद मान्यता'),
    )
    reject_reason = models.CharField(
        max_length=100,
        default='-',
        verbose_name=('नोंद नाकारल्यास त्याचे कारण'),
    )
    coordinator_note = models.TextField(
        default='-',
        verbose_name=('कोऑर्डिनेटरची टिप्पणी')
    )

    # def get_animals(self):
    #     animal_list = ''
    #     if self.OTHER_ANIMAL != self.animal_1:
    #         animal_list = animal_list + self.get_animal_1_display()
    #     if self.OTHER_ANIMAL != self.animal_2:
    #         animal_list = animal_list + ', ' + self.get_animal_2_display()
    #     if self.OTHER_ANIMAL != self.animal_3:
    #         animal_list = animal_list + ', ' + self.get_animal_3_display()
    #     if self.OTHER_ANIMAL != self.animal_4:
    #         animal_list = animal_list + ', ' + self.get_animal_4_display()

    #     return animal_list

    def get_animal_list(self):
        animal_list = ''
        for animal in self.animal:
            animal_list = animal_list + ' ' + animal + ','
        animal_list = animal_list.rstrip(',')
        return animal_list

    def __str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse('incident_detail', kwargs={'pk': self.pk})

