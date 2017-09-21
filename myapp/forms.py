from django import forms
from myapp.models import Topic
from myapp.models import Topic, Student


class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['subject','intro_course','avg_age','time']
        labels={'subject':'subject','intro_course':'This is an introductory level course','avg_age':'What is your age?','time':'Preferred Time'}
        widgets={'time':forms.RadioSelect}


class InterestForm(forms.Form):
    CHOICES=((1,'Yes'),(0,'No'))
    interested=forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES)
    age=forms.IntegerField(initial=20)
    comments=forms.CharField(widget=forms.Textarea,required=False,label='Additional Comments')

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['username','password','first_name','last_name','email','age','address','city', 'province','state']


class LoginForm(forms.Form):
    username=forms.CharField(label='username')
    password=forms.CharField(widget=forms.PasswordInput)