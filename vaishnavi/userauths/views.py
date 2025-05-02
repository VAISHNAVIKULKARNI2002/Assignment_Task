
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Note, Profile, Subscription

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    # Sample data for chart
    chart_data = {
        'labels': ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        'data': [5,9,7,8,6,10,4]
    }
    
    percent = 0
    if request.user.first_name: percent += 30
    if request.user.last_name: percent += 30
    if hasattr(request.user, 'profile') and request.user.profile.avatar and 'default.png' not in request.user.profile.avatar.url: percent += 40
    
    return render(request, 'dashboard.html', {'chart_data': chart_data})

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        # handle avatar
        avatar = request.FILES.get('avatar')
        if avatar:
            user.profile.avatar = avatar
            user.profile.save()
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'profile.html')

@login_required(login_url='login')
def notifications(request):
    notes = [
        {'msg': 'Welcome to the site!', 'time': '2025-04-27 10:00'},
        {'msg': 'Password changed successfully', 'time': '2025-04-26 09:15'},
        {'msg': 'New feature deployed', 'time': '2025-04-25 14:30'},
    ]
    return render(request, 'notifications.html', {'notifications': notes})

def faq(request):
    faqs = [
        {'q': 'How to register?', 'a': 'Click the Register button and fill the form.'},
        {'q': 'How to reset password?', 'a': 'Use Change Password in the navbar.'},
        {'q': 'How to contact support?', 'a': 'Go to Contact Us page.'},
    ]
    return render(request, 'faq.html', {'faqs': faqs})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us. We will respond soon.')
        return redirect('contact')
    return render(request, 'contact.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old = request.POST.get('old_psw')
        new = request.POST.get('new_psw')
        confirm = request.POST.get('confirm_psw')
        user = request.user
        if not user.check_password(old):
            messages.error(request, 'Old password is incorrect.')
        elif new != confirm:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('dashboard')
    return render(request, 'change_password.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('sub_email')
        if email:
            Subscription.objects.get_or_create(email=email)
            messages.success(request, 'Subscribed successfully!')
    return redirect(request.META.get('HTTP_REFERER','index'))


def reset_password(request):
    if request.method == 'POST':
        # Stub: send reset email
        messages.success(request, 'Password reset link sent to your email.')
        return redirect('login')
    return render(request, 'reset_password.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

@login_required(login_url='login')
def user_settings(request):
    if request.method == 'POST':
        messages.success(request, 'Settings saved.')
        return redirect('settings')
    return render(request, 'settings.html')

@login_required(login_url='login')
def activity_log(request):
    logs = [
        {'time':'2025-04-27 12:00','action':'Logged in'},
        {'time':'2025-04-26 18:30','action':'Updated profile'},
        {'time':'2025-04-25 09:15','action':'Changed password'},
    ]
    return render(request, 'activity_log.html', {'logs': logs})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def search(request):
    q = request.GET.get('q','')
    # stub search results
    results = [
        {'title': 'Getting Started', 'url': '#'},
        {'title': 'Profile Guide', 'url': '#'},
        {'title': 'FAQ', 'url': '#'},
    ]
    return render(request, 'search.html', {'query': q, 'results': results})

def testimonials(request):
    notes = [
        {'user':'Alice','text':'Great site, very intuitive!'},
        {'user':'Bob','text':'I love the dark mode feature.'},
        {'user':'Carol','text':'Excellent user experience.'},
    ]
    return render(request, 'testimonials.html', {'testimonials': notes})



@login_required(login_url='login')
def notes_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes_list.html', {'notes': notes})

@login_required(login_url='login')
def notes_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(user=request.user, title=title, content=content)
        return redirect('notes_list')
    return render(request, 'notes_create.html')

@login_required(login_url='login')
def notes_delete(request, note_id):
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if note:
        note.delete()
    return redirect('notes_list')
