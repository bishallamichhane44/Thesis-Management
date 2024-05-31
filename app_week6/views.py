from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .form import UserRegistrationForm, ThesisForm, GroupForm
from .models import Thesis, Group,User
from .form import UserLoginForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .form import ThesisForm  # Assuming you have a form for editing the thesis



@login_required
def delete_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, id=thesis_id)
    if request.user.user_type != 3 :
        return redirect('view_theses')
    if request.method == 'POST':
        thesis.delete()
        return redirect('view_theses')
    return render(request, 'app_week6/delete_thesis_confirm.html', {'thesis': thesis})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have signed up successfully.')
            return redirect('blank')
        else:
            cleaned_data = form.cleaned_data
            print("Form Response invalid:", cleaned_data)
    else:
        form = UserRegistrationForm()
    return render(request, 'app_week6/register.html', {'form': form})



  
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blank')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('home')
                pass
    else:
        form = UserLoginForm()
    return render(request, 'app_week6/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def upload_thesis(request):
    if ((request.user.user_type == 2) or (request.user.user_type == 1)):
        if request.method == 'POST':
            form = ThesisForm(request.POST)
            if form.is_valid():
                thesis = form.save(commit=False)
                thesis.supervisor = request.user
                thesis.save()
                return redirect('home')
        else:
            form = ThesisForm()
        return render(request, 'app_week6/upload_thesis.html', {'form': form})
    else:
        messages.error(request, "Not authorized to upload a thesis")
    return redirect('blank')

@login_required
def approve_thesis(request):
    if ((request.user.user_type == 3) or (request.user.user_type == 1)):
        theses = Thesis.objects.filter(is_approved=False)
        return render(request, 'app_week6/approve_thesis.html', {'theses': theses})
    if ((request.user.user_type != 3) and (request.user.user_type != 1)):
        messages.error(request, "Not authorized to approve a thesis")
    return redirect('blank')


@login_required
def view_theses(request):
    #if ((request.user.user_type == 3) or (request.user.user_type == 1)):
    theses = Thesis.objects.filter(is_approved=True)
    return render(request, 'app_week6/view_theses.html', {'theses': theses})
    return redirect('home')

@login_required
def create_group(request):
    if ((request.user.user_type == 2) or (request.user.user_type == 1)):
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                group = form.save()
                return redirect('home')
        else:
            form = GroupForm()
        return render(request, 'app_week6/create_group.html', {'form': form})
    if ((request.user.user_type != 2) and (request.user.user_type != 1)):
        messages.error(request, "Not authorized to create a group")
        return redirect('blank')


def blank(request):
    return render(request, 'app_week6/blank.html')
def home(request):
    return render(request, 'app_week6/home.html')

@login_required
def approve(request, thesis_id):
    thesis = Thesis.objects.get(pk=thesis_id)
    if ((request.user.user_type == 3) or (request.user.user_type == 1)):
        thesis.is_approved = True
        thesis.save()
        return redirect('view_theses')
    return redirect('blank')


@login_required
def thesis_detail(request, thesis_id):
    thesis = Thesis.objects.get(pk=thesis_id)
    if ((request.user.user_type == 1) or (request.user.user_type == 2) or (request.user.user_type == 3) or (request.user.user_type == 4)):
        return render(request, 'app_week6/thesis_detail.html', {'thesis': thesis})
    else:
        messages.error(request, "Not authorized to view thesis")
        return redirect('blank')



@login_required
def edit_thesis(request, thesis_id):
    thesis = Thesis.objects.get(pk=thesis_id)
    if ( request.user.user_type == 3):
        if request.method == 'POST':
            form = ThesisForm(request.POST, instance=thesis)
            if form.is_valid():
                form.save()
                return redirect('view_theses')
        else:
            form = ThesisForm(instance=thesis)
        return render(request, 'app_week6/edit_thesis.html', {'form': form})
    else:
        messages.error(request, "Not authorized to edit thesis")
        return redirect('home')




@login_required
def request_join(request, thesis_id):
    if ((request.user.user_type == 4) or (request.user.user_type == 1)):
        thesis = Thesis.objects.get(pk=thesis_id)
        thesis.interested.add(request.user)
        messages.success(request, "Request sent successfully")
        return redirect('view_theses')
    else:
        messages.error(request, "Not authorized to request to join")
        return redirect('view_theses')


@login_required
def approve_student(request, thesis_id, student_id):    
    
    if request.method == 'GET':
        student = User.objects.get(pk=student_id)
        thesis = Thesis.objects.get(pk=thesis_id)
        if ((request.user.user_type == 2) or (request.user.user_type == 3)):
            if((request.user.username == thesis.supervisor.username)or(request.user.user_type == 3)):
                print(thesis.students.count())
                if (thesis.students.count() < 5):
                    thesis.students.add(student)
                    thesis.interested.remove(student)
                    thesis.save()
                    messages.success(request, "Student added successfully")
                    return redirect('view_theses')
                else:
                    messages.error(request, "Cannot Add more than 5 students")
                    return redirect('view_theses')
            else:
                messages.error(request, "You are not the respective supervisor")
                return redirect('view_theses')

        else:
            messages.error(request, "Not authorized to approve a student")
            return redirect('view_theses')
    else:
        messages.error(request, "Invalid request")
        return HttpResponseRedirect(request.path_info)


@login_required
def your_theses(request):
    if ((request.user.user_type == 4)):
        theses = Thesis.objects.filter(students__in=[request.user])
        return render(request, 'app_week6/your_theses.html', {'theses': theses})
    else:
        messages.error(request, "Not authorized to view  theses")
        return redirect('blank')
