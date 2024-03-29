from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Question

from .forms import InstagramUserForm

from .test_get_page import PageAnalytics

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time

from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        print('123123')
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'


def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'name.html', context={'task_id': result.task_id})


def get_name(request):
    b = request.read()
    print(b)

    insta_username = ''
    try:
        insta_username = str(b, 'utf-8').split('username=')[1]
        print('Username = ', insta_username)
    except:
        pass
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InstagramUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            response = ''
            if insta_username:
                obj = PageAnalytics()

                response += obj.get_str_data(insta_username)

                subject = 'Test Instagram Analytics'
                message = response
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['oolleehh@gmail.com',]

                # send_mail( subject, message, email_from, recipient_list)

                url = obj.get_profile_pic(insta_username)

            # return HttpResponse(response, content_type='text/plain')
            return render(request, 'first/result.html', {'test' : obj.get_full_name(insta_username), 'result' : response , 'image_url' : url })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InstagramUserForm()

    return render(request, 'first/name.html', {'form': form})

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('first/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'first/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

