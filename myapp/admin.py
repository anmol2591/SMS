import re
from django.contrib import admin
from  .models import Author, Book, Student, Course, Topic
# Register your models here.

admin.site.register(Author)

#admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Topic)

class BookAdmin(admin.ModelAdmin):
    list_display=['title','author','numpages','in_stock']
admin.site.register(Book,BookAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','show_course']
    def show_course(self,obj):
        a=obj.course_set.all().values_list('title')
        s=str(a)
        return re.findall("'(.*?)'",s)

admin.site.register(Student,StudentAdmin)