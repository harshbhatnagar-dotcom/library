from django.contrib import admin
from . models import homeimage,Book,Student,Teacher,IssuedBook

admin.site.register(homeimage)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(IssuedBook)