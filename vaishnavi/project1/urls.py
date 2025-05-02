from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from userauths import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('settings/', views.user_settings, name='settings'),
    
    path('search/', views.search, name='search'),
    path('testimonials/', views.testimonials, name='testimonials'),    path('activity-log/', views.activity_log, name='activity_log'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/create/', views.notes_create, name='notes_create'),
    path('notes/delete/<int:note_id>/', views.notes_delete, name='notes_delete'),
    path('change-password/', views.change_password, name='change_password'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('logout/', views.logout_view, name='logout'),
]


# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'userauths.views.custom_404'
handler500 = 'userauths.views.custom_500'
