from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import homeimage, Book, Student, Teacher, IssuedBook, EJournal
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Home page
def index(request):
    images = homeimage.objects.all()
    return render(request, "libr/index.html", {"image": images})



# User login view
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'student'):
                return redirect('student_dashboard')
            elif hasattr(user, 'teacher'):
                return redirect('teacher_dashboard')
            else:
                return render(request, 'libr/login.html', {'error': 'No dashboard assigned'})
        else:
            return render(request, 'libr/login.html', {'error': 'Invalid credentials'})
    return render(request, 'libr/login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboards
@login_required
def student_dashboard(request):
    images = homeimage.objects.all()
    
    issued_books = []
    if hasattr(request.user, 'student'):
        issued_books = IssuedBook.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'image': images,
        'issued_books': issued_books,
    }
    return render(request, 'libr/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    images = homeimage.objects.all()

    issued_books = []
    if hasattr(request.user, 'teacher'):
        issued_books = IssuedBook.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'image': images,
        'issued_books': issued_books,
    }
    return render(request, 'libr/teacher_dashboard.html', context)

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'libr/admin_dashboard.html')

@login_required
def book(request):
    books = Book.objects.all()
    
    if hasattr(request.user, 'student'):
        dashboard_url = 'student_dashboard'
    elif hasattr(request.user, 'teacher'):
        dashboard_url = 'teacher_dashboard'
    elif request.user.is_superuser:
        dashboard_url = 'admin_dashboard'
    else:
        dashboard_url = 'home'  # fallback in case user type not identified

    return render(request, "libr/books.html", {"books": books, "dashboard_url": dashboard_url})

@login_required
def ejournal_list(request):
    journals = EJournal.objects.all().order_by('-added_on')

    if hasattr(request.user, 'student'):
        dashboard_url = 'student_dashboard'
    elif hasattr(request.user, 'teacher'):
        dashboard_url = 'teacher_dashboard'
    elif request.user.is_superuser:
        dashboard_url = 'admin_dashboard'
    else:
        dashboard_url = 'home'  # fallback in case user type not identified
    return render(request, 'libr/ejournal_list.html', {'journals': journals,"dashboard_url": dashboard_url})

@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        else:
            user.set_password(new_password)
            user.save()
            logout(request)  # Log out the user after password change
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('login')
        
    if hasattr(request.user, 'student'):
        dashboard_url = 'student_dashboard'
    elif hasattr(request.user, 'teacher'):
        dashboard_url = 'teacher_dashboard'
    elif request.user.is_superuser:
        dashboard_url = 'admin_dashboard'
    else:
        dashboard_url = 'home'  # fallback in case user type not identified   

    return render(request, 'libr/change_password.html',{"dashboard_url": dashboard_url})


# Add student
def add_student(request):
    if request.method == 'POST':
        student = Student(
            name=request.POST['name'],
            roll_number=request.POST['roll_number'],
            father_name=request.POST['father_name'],
            branch=request.POST['branch']
        )
        student.save()
        return redirect('add_student')
    return render(request, 'libr/add_student.html')

# Add teacher
def add_teacher(request):
    if request.method == 'POST':
        teacher = Teacher(
            name=request.POST['name'],
            employee_id=request.POST['employee_id'],
            department=request.POST['department']
        )
        teacher.save()
        return redirect('add_teacher')
    return render(request, 'libr/add_teacher.html')

# Add book
def add_book(request):
    if request.method == 'POST':
        book = Book(
            title=request.POST['title'],
            author=request.POST['author'],
            isbn=request.POST['isbn'],
            published_date=request.POST['published_date'],
            cover_image=request.FILES.get('cover_image')
        )
        book.save()
        return redirect('add_book')
    return render(request, 'libr/add_book.html')

# Issue or return book
def add_issued_book(request):
    users = User.objects.all()
    books = Book.objects.all()
    selected_user_id = request.GET.get('user_id')
    selected_user = None
    issued_books = None

    if selected_user_id:
        try:
            selected_user = User.objects.get(id=selected_user_id)
            issued_books = IssuedBook.objects.filter(user=selected_user)
        except User.DoesNotExist:
            selected_user = None

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'issue':
            user = User.objects.get(id=request.POST.get('user_id'))
            book = Book.objects.get(id=request.POST.get('book_id'))
            issue_date = timezone.now()
            return_date = issue_date + timedelta(days=15)
            IssuedBook.objects.create(
                user=user, book=book,
                issue_date=issue_date,
                return_date=return_date,
                returned=False
            )
            return redirect(f"{reverse('add_issued_book')}?user_id={user.id}")
        elif action == 'return':
            issued_book = IssuedBook.objects.get(id=request.POST.get('issued_id'))
            issued_book.returned = True
            issued_book.save()
            return redirect(f"{reverse('add_issued_book')}?user_id={issued_book.user.id}")

    return render(request, 'libr/add_issuedbook.html', {
        'users': users,
        'books': books,
        'selected_user': selected_user,
        'issued_books': issued_books,
    })

# Add homepage image
def add_homeimage(request):
    if request.method == "POST" and request.FILES.get("image"):
        homeimage.objects.create(image=request.FILES["image"])
        return redirect("add_homeimage")
    return render(request, "libr/add_homeimage.html")

#add ejournal
@login_required
def add_ejournal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        link = request.POST.get('link')
        upload = request.FILES.get('upload')

        if title and upload:
            EJournal.objects.create(
                title=title,
                description=description,
                upload=upload,
                link=link
            )
            return redirect('add_ejournal')

    return render(request, 'libr/add_ejournal.html')
