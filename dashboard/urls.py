from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('home', views.user_home, name='user_home'),
    path('logout', views.user_logout, name='user_logout'),
    path('profile', views.user_profile, name='user_profile'),
    path('update_password', views.update_password, name='update_password'),
    path('course', views.short_term_course, name='short_term_course'),
    path('course_create', views.short_term_course_create, name='short_term_course_create'),
    path('create_short_term_course', views.create_short_term_course, name='create_short_term_course'),
    path('delete_course', views.delete_course, name='delete_course'),
]