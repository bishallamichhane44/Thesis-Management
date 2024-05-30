# from django.shortcuts import render

# # Create your views here.


# # Expanded sample data with real thesis details
# mock_theses = [
#     {'id': 1, 'title': 'Machine learning approaches for Cyber Security', 'supervisor': 'Bharanidharan Shanmugam', 'short_description': 'Exploring machine learning in cyber security for risk modelling and prediction.', 'long_description': 'As we use the internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.'},
#     {'id': 2, 'title': 'Informetrics applications in multidisciplinary domain', 'supervisor': 'Yakub Sebastian', 'short_description': 'Quantitative studies of information in multidisciplinary research.', 'long_description': 'Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science, and bibliometric techniques on various information artifacts have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualization, and data wrangling tools.'},
#     {'id': 3, 'title': 'Development of a Virtual Reality System to Test Binaural Hearing', 'supervisor': 'Sami Azam', 'short_description': 'Designing a VR system to test binaural hearing abilities.', 'long_description': 'A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off-the-shelf components (VR goggle and headphones) and standard programming techniques.'},
#     {'id': 4, 'title': 'Current trends on cryptomining and its potential impact on cryptocurrencies', 'supervisor': 'Sami Azam', 'short_description': 'Exploring cryptomining trends and their impact on cryptocurrencies.', 'long_description': 'Cryptomining is the process of mining cryptocurrencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out what type of crypto mining methodologies are being applied, apart from crypto-mining, what other security risks may it introduce, and how current web standards are tackling this problem.'},
#     {'id': 5, 'title': 'Artificial Intelligence in Health Informatics', 'supervisor': 'Artificial Intelligence in Health Informatics', 'short_description': 'Utilizing AI to analyze health datasets for predictive modeling.', 'long_description': 'The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.'},
#     {'id': 6, 'title': 'Unsupervised Model Development from Autism Screening Data', 'supervisor': 'Asif Karim', 'short_description': 'Developing a two-cluster solution for autism screening.', 'long_description': 'The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.'},
#     {'id': 7, 'title': 'Applying Artificial Intelligence to solve real world problems', 'supervisor': 'Bharanidharan Shanmugam', 'short_description': 'Exploring AI applications in solving real-world problems.', 'long_description': 'Artificial Intelligence has been used in many applications to solve certain problems throughout academia and the industry  from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include building a bot, predicting the power usage, spam filtering and the list is endless.'}
# ]

# def thesis_list(request):
#     return render(request, 'app_week6/thesis_list.html', {'theses': mock_theses})

# def thesis_details(request, thesis_id):
#     thesis = next((item for item in mock_theses if item['id'] == thesis_id), None)
#     if thesis is None:
#         return render(request, '404.html', {'error': "The requested thesis does not exist."})
#     return render(request, 'app_week6/thesis_details.html', {'thesis': thesis})

# def home(request):
#     return render(request, 'app_week6/index.html')

# def about(request):
#     team_data = {
        
#             'name_1': 'Sujan Kandel', 'student_id_1': 'S360707', 
#             'name_2': 'Nikesh Poudel', 'student_id_2': 'S362818',
#             'name_3': 'Sanish Thakur', 'student_id_3': 'S362084',
#             'name_4': 'Ajay Adhikari', 'student_id_4': 'S361935',
        
#     }
#     return render(request,'app_week6/about.html', team_data)


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .form import UserRegistrationForm, ThesisForm, GroupForm
from .models import Thesis, Group
from .form import UserLoginForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have signed up successfully.')
            return redirect('home')
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
                return redirect('home')
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
    return redirect('home')

@login_required
def approve_thesis(request):
    if ((request.user.user_type == 3) or (request.user.user_type == 1)):
        theses = Thesis.objects.filter(is_approved=False)
        return render(request, 'app_week6/approve_thesis.html', {'theses': theses})
    if ((request.user.user_type != 3) and (request.user.user_type != 1)):
        messages.error(request, "Not authorized to approve a thesis")
    return redirect('home')


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
        return redirect('home')




def home(request):
    return render(request, 'app_week6/base.html')

@login_required
def approve(request, thesis_id):
    thesis = Thesis.objects.get(pk=thesis_id)
    if ((request.user.user_type == 3) or (request.user.user_type == 1)):
        thesis.is_approved = True
        thesis.save()
        return redirect('view_theses')
    return redirect('home')


@login_required
def thesis_detail(request, thesis_id):
    thesis = Thesis.objects.get(pk=thesis_id)
    if ((request.user.user_type == 1) or (request.user.user_type == 2) or (request.user.user_type == 3) or (request.user.user_type == 4)):
        return render(request, 'app_week6/thesis_detail.html', {'thesis': thesis})
    else:
        messages.error(request, "Not authorized to view thesis")
        return redirect('home')
