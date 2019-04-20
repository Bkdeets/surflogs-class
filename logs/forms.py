
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Session, Report, Wave_Data, Photo, Spot
from django.contrib.auth.forms import UserCreationForm, User
from PIL import Image
from bootstrap_modal_forms.forms import BSModalForm

TIDES = (
    ('L','Low'),
    ('LR','Low Rising'),
    ('MR','Mid Rising'),
    ('H','High'),
    ('HF','High Falling'),
    ('MF','Mid Falling')
)

CROWDS = (
    ('Solo','Solo'),
    ('Light','Light'),
    ('Medium','Medium'),
    ('Heavy','Heavy'),
    ('Packed','Packed')
)

DIRECTIONS = (
    ('S','S'),
    ('SSW','SSW'),
    ('SW','SW'),
    ('WSW','WSW'),
    ('W','W'),
    ('WNW','WNW'),
    ('NW','NW'),
    ('NNW','NNW'),
    ('N','N'),
    ('NNE','NNE'),
    ('NE','NE'),
    ('ENE','ENE'),
    ('E','E'),
    ('ESE','ESE'),
    ('SE','SE'),
    ('SSE','SSE'),
)

CONDITIONS = (
    ('Glassy','Glassy'),
    ('Groomed','Groomed'),
    ('Textured','Textured'),
    ('Bumpy','Bumpy'),
    ('Choppy','Choppy'),
    ('VAS','Victory At Sea')
)

RATINGS = [(x,x) for x in range(1,11)]

SPOT_TYPES = (
    ('Beach','Beach'),
    ('Reef','Reef'),
    ('Point','Point'),
    ('Slab','Slab'),
    ('Pool','Pool'),
    ('Wedge','Wedge')
)

WAVE_QUALITY = (
    ('Dismal','Dismal'),
    ('Poor','Poor'),
    ('Fair','Fair'),
    ('Good','Good'),
    ('Great','Great'),
    ('Epic','Epic'),
)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1'
        )

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

class ProfileForm(ModelForm):
    #hide_stats = forms.Checkbox()
    class Meta:
        model = Profile
        fields = (
            'homespot',
            'bio',
            'photo'
        )

class NewSpotForm(ModelForm):
    ideal_tide =         forms.ChoiceField(choices=TIDES,required=False)
    ideal_swell_dir =    forms.ChoiceField(choices=DIRECTIONS,required=False)
    ideal_wind_dir =    forms.ChoiceField(choices=DIRECTIONS,required=False)
    type =               forms.ChoiceField(choices=SPOT_TYPES)

    class Meta:
        model = Spot
        fields = (
            'name',
            'type',
            'location',
            'ideal_tide',
            'ideal_wind_dir',
            'ideal_swell_dir',
            'ideal_swell_height',
            'ideal_swell_period'
        )

class SessionForm(ModelForm):
    waves_caught = 	 forms.IntegerField(required=False)
    rating =         forms.ChoiceField(choices=RATINGS,required=False)
    class Meta:
        model = Session
        fields = (
            'date',
            'start_time',
            'end_time',
            'spot',
            'waves_caught',
            'rating',
            'notes'
        )
        widgets = {
            'date': forms.DateTimeInput( attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }),
            'start_time': forms.TimeInput( attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker3'
            }),
            'end_time': forms.TimeInput( attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker4'
            })
        }

class ReportForm(ModelForm):

    wave_quality = forms.ChoiceField(choices=WAVE_QUALITY)

    class Meta:
        model = Report
        fields = (
            'date',
            'time',
            'spot',
            'wave_quality',
            'notes'
        )
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker2'
                    }
            ),
            'time': forms.DateTimeInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker3'
                    }
            )
        }

class WaveDataForm(ModelForm):
    tide =          forms.ChoiceField(choices=TIDES,required=False)
    crowd =         forms.ChoiceField(choices=CROWDS,required=False)
    wind_dir =      forms.ChoiceField(choices=DIRECTIONS,required=False)
    wave_height =   forms.IntegerField(required=False)
    wave_period =   forms.CharField(required=False)
    wind_speed =    forms.CharField(required=False)
    conditions =    forms.ChoiceField(choices=CONDITIONS,required=False)
    class Meta:
        model = Wave_Data
        fields = (
            'tide',
            'crowd',
            'wind_dir',
            'wave_height',
            'wave_period',
            'wind_speed',
            'conditions',
            'spot'
        )

class ImageUploadForm(ModelForm):
    class Meta:
        model = Photo
        fields = (
            'image',
        )
