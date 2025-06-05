from django.db import models
from django.utils import timezone
from datetime import timedelta

from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class homeimage(models.Model):
    image = models.ImageField(upload_to="libr/images", default="")

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    cover_image = models.ImageField(upload_to="libr/book_covers", default="")
    
    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name=models.CharField(max_length=100,default="")
    roll_number = models.CharField(max_length=20, unique=True)
    father_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.user:
            base_username = f"{self.name.lower()}123"
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Create the user with username and password same as username
            user = User.objects.create_user(username=username, password=username)
            self.user = user
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Student: {self.user.username if self.user else 'No user'}"

    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name= models.CharField(max_length=100 ,default="")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)

    

    def save(self, *args, **kwargs):
        if not self.user:
            base_username = f"{self.name.lower()}123"

            # Ensure username uniqueness
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(username=username, password=username)
            self.user = user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Teacher: {self.user.username if self.user else 'No user'}"


class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # student or teacher
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(default=timezone.now() + timedelta(days=15))
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({'Returned' if self.returned else 'Not Returned'})"

class EJournal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='ejournals/')
    link = models.URLField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
