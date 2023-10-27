from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
        
            return JsonResponse({'error': 'Username or Password is Incorrect'}, status=400)

    return render(request, 'login.html')

@never_cache
def user_home(request):
    if request.user.is_authenticated:
        return render(request,'index.html')

    return redirect(user_login)

@never_cache
def user_logout(request):
    logout(request)
    return redirect(user_login)

@never_cache
def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        custom_user = CustomUser.objects.get(pk = user.id)
        context = {"user": custom_user}
        return render(request,'profile.html', context)

    return redirect(user_login)

@never_cache
@csrf_exempt
def update_password(request):
    if request.user.is_authenticated and request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if the current password is correct
        if not request.user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            return JsonResponse({'error': 'New password and confirmation do not match'}, status=400)

        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update the user's session
        update_session_auth_hash(request, request.user)

        return JsonResponse({'message': 'Password updated successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@never_cache
def short_term_course(request):
    if request.user.is_authenticated:
        user = request.user
        courses = ShortTermCourse.objects.filter(user=user).order_by('-id')
        context = {"courses": courses}
        return render(request,'short-course-view.html', context)

    return redirect(user_login)

@never_cache
def short_term_course_create(request):
    if request.user.is_authenticated:
        user = request.user
        all_courses = ShortTermCourse.objects.filter(user=user)

        return render(request,'short-course-create.html')

    return redirect(user_login)

@csrf_exempt
def create_short_term_course(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            image = None
            try:
                if len(request.FILES['image'] ) != 0:
                    image = request.FILES['image']
            except:
                pass    
            title = request.POST['title']
            subtitle = request.POST['subtitle']
            description = request.POST['description']
            amount = request.POST['amount']
            status_str = request.POST['status']
            status = False if status_str.lower() == 'false' else True

            ShortTermCourse.objects.create(user = user,
                title = title,
                subtitle = subtitle,
                amount = amount,
                description = description,
                image = image,
                status = status
            )
            
            return JsonResponse({'message': 'Short term course created'}, status=200)
    
    else:
        return redirect(user_login)

@csrf_exempt
def delete_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        try:
            course = ShortTermCourse.objects.get(pk=course_id)
            course.delete()
            return JsonResponse({'success': True, 'message': 'Course deleted successfully'})
        except ShortTermCourse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Course not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})