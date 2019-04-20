### Imports ####################################################################
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session,Report,Spot,Profile,Photo,UserSummary
import numpy as np
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from itertools import chain
from .sql import RawOperations
import datetime
from django.utils import timezone
from PIL import Image
from bootstrap_modal_forms.generic import BSModalCreateView
################################################################################
SESSION_HEADERS = ["User","Date","Spot","Start","End","Rating"]
REPORT_HEADERS = ["User","Date","Spot","Time","Quality"]




### Signup View #################################################################
def signup(request):
    sessions = Session.objects.all()
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    errors = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()
            user.profile.homespot = Spot.objects.filter(name='Pipeline')[0]
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_summary = UserSummary(user.id, user.username)
            user_summary.save()
            return redirect('logs:profile_edit')
        else:
            errors = form.errors
    else:
        form = UserForm()

    context = {
        'sessions': sessions,
        'user':user,
        'user_form':form,
        'errors':errors,
    }
    return render(request, 'logs/signup.html', context)
################################################################################



### Index ######################################################################
def index(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None

    return render(request, 'index.html', {'user':user})
################################################################################


### Signin View ################################################################
def signin(request):
    errors = ''
    username = password = ''
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    if request.POST:
        form = SigninForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)

            if user is not None:
                profile = Profile.objects.filter(user=user)
                if profile:
                    login(request, user)
                    return redirect('logs:profile')
                else:
                    profile = Profile(user=user)
                    login(request, user)
                    return redirect('logs:profile_edit')
        else:
            errors = form.errors
    else:
        form = SigninForm()

    context = {
        'signin_form':form,
        'errors':errors,
    }
    return render(request, 'logs/signin.html', context)
################################################################################



### Detail View ################################################################
def detail(request, session_id):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    session = get_object_or_404(Session, pk=session_id)
    timeSurfed = totalTime([session])
    time_surfed_tuples = []
    for key,val in enumerate(timeSurfed.values()):
        if val[1] > 0:
            time_surfed_tuples.append(val)

    raw_op = RawOperations()
    photos = Photo.objects.filter(referencing_id=session_id)

    context = {
        'session':session,
        'time_surfed_tuples':time_surfed_tuples,
        'is_users': user == session.user,
        'photos':photos,
        'user':user,
    }
    return render(request, 'logs/detail.html', context)
################################################################################


### CSC 455 Version ###
### Profile View ###############################################################
def profile(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    if user:
        userImage = user.profile.photo
        raw_op = RawOperations()

        ## View for user? ##
        ## can make an sql function with this ##
        sessions = Session.objects.raw('SELECT * FROM logs_session WHERE user_id = %s ORDER BY date',[user.id])[::-1]
        reports = Report.objects.filter(user_id = user.id)

        ## Aggregate queries
        numSessions = raw_op.execSQL('SELECT COUNT(*) FROM logs_session WHERE user_id = %s',[user.id])[0][0]
        waveCount = raw_op.execSQL('SELECT SUM(waves_caught) FROM logs_session WHERE user_id = %s',[user.id])[0][0]
        averageRating = raw_op.execSQL('SELECT AVG(rating) FROM logs_session WHERE user_id = %s',[user.id])[0][0]

        ## Nested queries
        averageWaveHeight = raw_op.execSQL('SELECT AVG(wave_height) FROM logs_wave_data WHERE (SELECT wave_data_id FROM logs_session WHERE user_id = %s) = logs_wave_data.wave_data_id;',[user.id])[0][0]

        ## Stored function?
        #raw_op.build_stored_functions()
        #level = raw_op.execSQL('UserLevel(%s)',[numSessions])
        #print(level)

        ## Needs time operations queries
        if numSessions > 0:
            lastSpot = Session.objects.filter(user=user).latest('date').spot
        else:
            lastSpot = None

        if len(sessions) > 0:
            avgSessionLength = averageTimeSurfed(sessions)
            avgStartTime = averageTime([s.start_time for s in sessions])
            avgEndTime = averageTime([s.end_time for s in sessions])
        else:
            avgSessionLength = 0
            avgStartTime = 0
            avgEndTime = 0

        timeSurfed = totalTime(sessions)
        maxim = ("No Sessions"," ")
        for key,val in enumerate(timeSurfed.items()):
            if val[1][1] > 0:
                maxim = val[1]
                break
        timeSurfed = maxim[1]
        unitsSurfed = maxim[0]


        users = User.objects.all()
        context = {
            'user':user,
            'sessions':sessions,
            'reports':reports,
            'numSessions':numSessions,
            'waveCount':waveCount,
            'averageRating':averageRating,
            'lastSpot':lastSpot,
            'avgSessionLength':avgSessionLength,
            'timeSurfed':timeSurfed,
            'unitsSurfed':unitsSurfed,
            'averageWaveHeight':averageWaveHeight,
            'avgStartTime':avgStartTime,
            'avgEndTime':avgEndTime,
            'users': users
        }
        return render(request, 'logs/profile.html',context)
    else:
        return redirect('logs:login')
################################################################################



### Profile and User Edit View #################################################
def profileEdit(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    profile = Profile.objects.filter(user=user)[0]
    errors = ''

    if user:
        if request.method == 'POST':
            user_edit_form = UserEditForm(data=request.POST, instance=request.user)
            profile_edit_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if user_edit_form.is_valid() and profile_edit_form.is_valid():
                user = user_edit_form.save()
                profile = profile_edit_form.save()
                profile.save()
                user_summary = UserSummary.objects.filter(username=user.username)
                if user_summary:
                    user_summary = user_summary[0]
                    user_summary.username = user.username
                    user_summary.bio = profile.bio
                    user_summary.homespot = profile.homespot
                    user_summary.photo = profile.photo
                    user_summary.save()
                else:
                    user_summary = UserSummary(
                        user.id,
                        user.username,
                        profile.bio,
                        profile.homespot,
                        profile.photo
                        )
                    user_summary.save()

                return redirect('logs:profile')
            else:
                errors = [user_edit_form.errors, profile_edit_form.errors]
        else:
            user_fields = {
                'username':  user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
             }
            profile_fields = {
                'user':user,
                'homespot':  profile.homespot,
                'bio': profile.bio,
             }
            user_edit_form = UserEditForm(user_fields, instance=request.user)
            profile_edit_form = ProfileForm(profile_fields, instance=profile)

    context = {
        'user': user,
        'errors': errors,
        'profile_edit_form': profile_edit_form,
        'user_edit_form': user_edit_form,
    }
    return render(request, 'logs/profile_edit.html', context)
################################################################################



### Feed View ##################################################################
def feed(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None

    sessions = Session.objects.order_by('-date')[:30]
    sessions_with_image = []
    for session in sessions:
        photos = Photo.objects.filter(referencing_id=session.session_id)
        photo = None
        if photos:
            for photo1 in photos:
                last = str(photo1.image).split("/")[-1]
                if last != 'no-img.jpg':
                    photo = photo1
                    break
        sessions_with_image.append((session,photo))


    reports = Report.objects.order_by('-date')[:30]
    context = {
        'user':user,
        'sessions':sessions,
        'sessions_with_image':sessions_with_image,
        'reports':reports,
        'session_headers':SESSION_HEADERS,
        'report_headers':REPORT_HEADERS
    }

    return render(request, 'logs/feed.html', context)
################################################################################



### Session List ##################################################################
def session_list(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None

    sessions = Session.objects.order_by('date')[:30]
    sessions = sessions[::-1]
    headers = [
        'User',
        'Date',
        'Spot',
        'Start',
        'End',
        'Rating'
    ]
    context = {
        'user':user,
        'sessions':sessions,
        'headers':headers,
    }
    return render(request, 'logs/session_list.html', context)
################################################################################



### Login Redirect #############################################################
def login_success(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    profile = Profile.objects.filter(user=user)[0]

    if profile:
        # user is an admin
        return redirect('logs:profile')
    else:
        return redirect('logs:profile_edit')
################################################################################



### Post Session ###############################################################
def post_session(request):
    errors = ''
    if request.user and request.user.username != '':
        user = request.user
    else:
        return redirect('logs:signin')
    if user:
        if request.method == 'POST':
            print(request.FILES)
            session_post_form = SessionForm(request.POST)
            wave_data_form = WaveDataForm(request.POST)
            new_spot_form = NewSpotForm(request.POST)
            image_form = ImageUploadForm(request.POST, request.FILES)

            if session_post_form.is_valid() and wave_data_form.is_valid() and image_form.is_valid():
                session = session_post_form.save(commit=False)
                wave_data = wave_data_form.save(commit=False)
                photo = image_form.save()
                print(photo.image)

                wave_data.spot = session.spot
                wave_data.date = session.date
                wave_data.time = session.end_time

                session.user = user
                wave_data.save()
                session.wave_data = wave_data
                session.save()
                photo.referencing_id = session.session_id
                photo.save()
                print(photo.image)

                return redirect('logs:detail',session.session_id)

            else:
                errors = [
                        session_post_form.errors,
                        wave_data_form.errors,
                        image_form.errors
                ]
        else:
            session_post_form = SessionForm()
            wave_data_form = WaveDataForm()
            new_spot_form = NewSpotForm()
            image_form = ImageUploadForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'type':"Post",
        'session_post_form':session_post_form,
        'wave_data_form':wave_data_form,
        'new_spot_form':new_spot_form,
        'image_form':image_form,
        'errors':errors
    }

    return render(request, 'logs/post_session.html', context)
################################################################################


### edit Session ###############################################################
def edit_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    errors = ''
    if request.user and request.user.username != '':
        user = request.user
    else:
        return redirect('logs:signin')
    if user:
        if request.method == 'POST':
            session_post_form = SessionForm(request.POST, instance=session)
            wave_data_form = WaveDataForm(request.POST, instance=session.wave_data)
            new_spot_form = NewSpotForm(request.POST)
            image_form = ImageUploadForm(request.POST, request.FILES)
            print(request.FILES)
            if session_post_form.is_valid() and wave_data_form.is_valid() and image_form.is_valid():

                session = session_post_form.save(commit=False)
                wave_data = wave_data_form.save(commit=False)
                photo = image_form.save()
                print(photo.image)
                print(request.FILES)

                wave_data.spot = session.spot
                wave_data.date = session.date
                wave_data.time = session.end_time

                session.user = user
                wave_data.save()
                session.wave_data = wave_data
                session.save()
                print(session.session_id)
                photo.referencing_id = session.session_id
                photo.save()

                return redirect('logs:detail',session.session_id)

            else:
                errors = [
                        session_post_form.errors,
                        wave_data_form.errors,
                        image_form.errors
                ]
        else:
            session_post_form = SessionForm(instance=session)
            wave_data_form = WaveDataForm(instance=session.wave_data)
            new_spot_form = NewSpotForm()
            image_form = ImageUploadForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'type':"Edit",
        'session_post_form':session_post_form,
        'wave_data_form':wave_data_form,
        'new_spot_form':new_spot_form,
        'image_form':image_form,
        'errors':errors
    }

    return render(request, 'logs/post_session.html', context)
################################################################################

### add photos ###############################################################
def add_photos(request, session_id):
    errors = ''
    if request.user and request.user.username != '':
        user = request.user
    else:
        return redirect('logs:signin')

    if user:
        if request.method == 'POST':
            image_form = ImageUploadForm(request.POST, request.FILES)

            if image_form.is_valid():
                photo = image_form.save()
                photo.referencing_id = session_id
                photo.save()
                return redirect('logs:detail', session_id)

            else:
                errors = [
                        image_form.errors
                ]
        else:
            image_form = ImageUploadForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'image_form':image_form,
        'errors':errors
    }

    return render(request, 'logs/add_photos.html', context)
################################################################################


### Report #####################################################################
def report(request, report_id):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    report = get_object_or_404(Report, pk=report_id)

    context = {
        'report':report,
        'user':user
    }
    return render(request, 'logs/report.html', context)
################################################################################



###Create new spot###############################################################
def create_spot(request):
    print("got here")
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    print(user)
    errors = ''
    if user:
        if request.method == 'POST':
            new_spot_form = NewSpotForm(request.POST)
            if new_spot_form.is_valid():
                spot = new_spot_form.save()
                spot.save()
                return redirect('logs:autoclose')
            else:
                errors = new_spot_form.errors
        else:
            new_spot_form = NewSpotForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'new_spot_form':new_spot_form,
        'errors':errors
    }

    return render(request, 'logs/spot_create.html', context)
################################################################################


### Post Report ###############################################################
def post_report(request):
    raw_op = RawOperations()
    raw_op.create_trigger()
    errors = ''
    if request.user and request.user.username != '':
        user = request.user
    else:
        return redirect('logs:signin')
    if user:
        if request.method == 'POST':
            report_post_form = ReportForm(request.POST)
            wave_data_form = WaveDataForm(request.POST)

            if report_post_form.is_valid() and wave_data_form.is_valid():

                # Calling raw sql to do an INSERT operation with Prepared Statements

                # report_id = raw_op.processReportFormAndReturnId(report_post_form=report_post_form, user=user.id)
                # report = Report.objects.filter(report_id=report_id)[0]
                report = report_post_form.save(commit=False)
                wave_data = wave_data_form.save(commit=False)

                report.user = user

                wave_data.date = report.date
                wave_data.spot = report.spot
                wave_data.save()
                report.wave_data = wave_data
                report.save()

                return redirect('logs:profile')

            else:
                errors = report_post_form.errors

        else:
            report_post_form = ReportForm()
            wave_data_form = WaveDataForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'report_post_form':report_post_form,
        'wave_data_form':wave_data_form,
        'errors':errors
    }

    return render(request, 'logs/post_report.html', context)
################################################################################




### Upload Profile Image #######################################################
def upload_profile_pic(request):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    profile = user.profile
    errors = ''

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            return redirect('logs:profile')
        else:
            errors = form.errors
    else:
        form = ImageUploadForm({'referencing_id':user.id})


    context = {
        'user':user,
        'form':form,
        'errors':errors
    }
    return render(request, 'logs/upload_photo.html', context)
################################################################################



### User Summary View #######################################################
def user_summary(request, username="default"):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None
    if user.username != username:
        assoc_user = User.objects.filter(username=username)[0]
        user_summary = UserSummary.objects.filter(username=username)
        if len(user_summary) > 0:
            user_summary = user_summary[0]
        sessions = []
        context = {
            'user_summary' : user_summary,
            'assoc_user' : assoc_user,
            'sessions' : sessions,
            'user' :user
        }
        return render(request, 'logs/user_summary.html', context)
    else:
        return redirect('logs:profile')
################################################################################



### Spot View #######################################################
def spot_view(request, spot_name="default"):
    if request.user and request.user.username != '':
        user = request.user
    else:
        user = None

    spot = Spot.objects.filter(name=spot_name)[0]
    sessions = Session.objects.filter(spot=spot)[::-1]
    print(spot_name)
    print(spot)
    context = {
        'spot' : spot,
        'sessions' : sessions,
        'numSessions' : len(sessions),
        'numSurfers' : len(sessions), #Opportunity to have an SQL
        'user' : user
    }
    return render(request, 'logs/spot_view.html', context)
################################################################################



## autoclose ############################################################
def autoclose(request):
    return render(request, 'logs/autclose.html')
################################################################################



### Helper Functions ############################################################
def averageTimeSurfed(sessions):
    count = len(sessions)
    t_hours = 0
    for session in sessions:
        t_hours += (session.end_time.hour - session.start_time.hour)*60
        t_hours += session.end_time.minute - session.start_time.minute
        t_hours += (session.end_time.second - session.start_time.second)//60
    return t_hours//count


def averageTime(times):
    total_sec = 0
    for time in times:
        seconds_from_midnight = (time.hour*60*60) + (time.minute*60) + time.second
        total_sec += seconds_from_midnight
    avg_sec = total_sec//len(times)

    avg_hours = avg_sec//60//60
    avg_minutes = (avg_sec//60) - (avg_hours*60)
    avg_sec = avg_sec - (avg_minutes*60) - (avg_hours*60*60)


    return datetime.time(hour=avg_hours, minute=avg_minutes, second=avg_sec)


def totalTime(sessions):
    t_seconds = 0
    for session in sessions:
        t_seconds += (session.end_time.hour - session.start_time.hour)*60*60
        t_seconds += (session.end_time.minute - session.start_time.minute)*60
        t_seconds += session.end_time.second - session.start_time.second

    t_minutes = t_seconds//60
    t_hours = t_minutes//60
    t_days = t_hours//24
    t_weeks = t_days//7

    weeks = t_weeks
    days = t_days - weeks*7
    hours = t_hours - days*24
    minutes = t_minutes - hours*60

    total_time = {
        'weeks':('Weeks',weeks),
        'days':('Days',days),
        'hours':('Hours',hours),
        'minutes':('Minutes',minutes)
    }

    return total_time




################################################################################
