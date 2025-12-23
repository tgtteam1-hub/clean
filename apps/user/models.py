# from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from apps.user.managers import UserManager


def char_is_number(value):
    print(str(value).isdigit)
    if str(value).isdigit():
        return value
    else:
        raise ValidationError('Not a number')


class User(PermissionsMixin, AbstractBaseUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ('username',)
    objects = UserManager()

    # Role options
    MEMBER = 1
    WATCHER = 2
    COORDINATOR = 3
    MANAGER = 4
    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (WATCHER, 'Watcher'),
        (COORDINATOR, 'Coordinator'),
        (MANAGER, 'Manager'),
    )

    # Gender options
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    )

    # Occupation options
    FOREST_LABOUR = 1
    SHEPHARD = 2
    PRIVATE_JOB = 3
    FARMER = 4
    FOREST_DEPARTMENT = 5
    STUDENT = 6
    OCCUPATION_OTHER = 7
    OCCUPATION_CHOICES = (
        (FOREST_LABOUR, 'Forest Labour'),
        (SHEPHARD, 'Shephard'),
        (PRIVATE_JOB, 'Private Job'),
        (FARMER, 'Farmer'),
        (FOREST_DEPARTMENT, 'Forest Department'),
        (STUDENT, 'Student'),
        (OCCUPATION_OTHER, 'Other'),
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=('username'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        default=2
    )
    name = models.CharField(
        max_length=50,
        default = '-',
        verbose_name=('name'),
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES,
        default=1
    )
    age = models.PositiveSmallIntegerField(
        default = 1,
    )
    occupation = models.PositiveSmallIntegerField(
        choices=OCCUPATION_CHOICES,
        default=2
    )
    village = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('Village'),
    )
    taluka = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('Taluka'),
    )
    district = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('District'),
    )
    state = models.CharField(
        max_length=100,
        default = '-',
        verbose_name=('State'),
    )
    pin_code = models.PositiveIntegerField(
        default = 0,
        validators=[
            MaxValueValidator(999999),
         ]
    )
    mobile_number_1 = models.CharField(
        max_length=10,
        validators=[
            char_is_number,
         ],
        default = '0'
    )
    mobile_number_2 = models.CharField(
        max_length=10,
        validators=[
            char_is_number,
         ],
        default = '0',
        null = True,
        blank = True,

    )
    profile_picture = models.ImageField(
        default = 'profile_pics/default.jpg',
        upload_to = 'profile_pics'
    )


    def __str_(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

