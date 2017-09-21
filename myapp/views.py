from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Author, Book, Course,Student, Topic
from django.shortcuts import get_object_or_404
from myapp.forms import TopicForm, InterestForm, StudentForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    courselist = Course.objects.all().order_by('course_no')[:10]
    return render(request, 'myapp/index.html', {'courselist': courselist})


def about(request):

    return render(request,'myapp/about.html')

def detail(request,course_no):
    #response=HttpResponse()
    course=get_object_or_404(Course,course_no=course_no)
    return render(request,'myapp/detail.html',{'course':course})


def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topics.html', {'topiclist':   topiclist})

def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = TopicForm()
    return render(request, 'myapp/addtopic.html', {'form': form,
                                                   'topiclist': topiclist})


def topicdetail(request,topic_id):
    topicdetail=get_object_or_404(Topic,id=topic_id)
    if request.method=='POST':
        interestform=InterestForm(request.POST)
        if interestform.is_valid():
            if interestform.cleaned_data['interested']=='1':
                form=TopicForm(instance=topicdetail)
                topic=form.save(commit=False)
                topic.num_responses=topic.num_responses+1
                topic.avg_age=(topic.avg_age*(topic.num_responses)+interestform.cleaned_data['age'])/(topic.num_responses+1)
                topic.save()
                return HttpResponseRedirect(reverse('myapp:topics'))
            else:
                return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form=InterestForm()
        return render(request,'myapp/topicdetail.html',{'form':form, 'topicdetail':topicdetail})

def register(request):
    if request.method == 'POST':
        stuform = StudentForm(request.POST)
        if stuform.is_valid():
            user=stuform.save(commit=False)
            user.set_password(stuform.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('myapp:index'))
    else:
        form=StudentForm()
        return render(request,'myapp/register.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index')) #
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        form=LoginForm()
        return render(request, 'myapp/login.html',{'requser':request.user,'form':form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))



def mycourses(request):
        l=len(Student.objects.filter(username = request.user.username))
        if l==1:
            student=Student.objects.get(username=request.user.username)
            course=student.course_set.all()

            return render(request, 'myapp/mycourses.html', {'course': course,'flag':0})
        else:

            return render(request, 'myapp/mycourses.html', {'flag': 1})


