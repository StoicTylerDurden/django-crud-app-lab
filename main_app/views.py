from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plant, Care
from .forms import CareForm  
from django.contrib.auth.views import LoginView


from django.views.generic import ListView, DetailView
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginView):
    template_name = 'home.html'


class PlantCreate(LoginRequiredMixin , CreateView):
    model = Plant
    fields = '__all__'
    success_url = '/plants/'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = ['species', 'description', 'age']

class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/'

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

@login_required
def plant_index(request):
    plants =  Plant.objects.filter(user=request.user)
    return render(request, 'plants/index.html', { 'plants': plants })

def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    care_form = CareForm()
    care_actions = Care.objects.filter(plant=plant)  

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'care_form': care_form,
        'care_actions': care_actions
    })    

@login_required
def add_care(request, plant_id):
    form = CareForm(request.POST)
    if form.is_valid():
        new_care = form.save(commit=False)
        new_care.plant_id = plant_id
        new_care.save()
    return redirect('plant-detail', plant_id=plant_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('plant-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )