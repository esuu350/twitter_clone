from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . models import Profile, Twitt
from . forms import TwittForm, SighUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User


def home(request):
    
    if request.user.is_authenticated:
        form = TwittForm(request.POST or None, request.FILES)
    
        if request.method == "POST":
            
            if form.is_valid():
                twitt = form.save(commit = False)
                twitt.user = request.user
                twitt.save()
                messages.success(request, ("You have twitted!"))
                return redirect('home')
           

        twitts = Twitt.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"twitts": twitts, "form": form})
    else:
        twitts = Twitt.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"twitts": twitts})
    
   


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("Please Log In First!"))
        return redirect('home')
    

    

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        twitts = Twitt.objects.filter(user_id = pk)

        if request.method == "POST":

            current_user_profile = request.user.profile

            action = request.POST['follow']

            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save

        return render(request, "profile.html", {"profile": profile, "twitts": twitts})


    else:
        messages.success(request, ("Please Log In First!"))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login Succesful!"))
            return redirect('home')
        else:
            messages.success(request, ("Please try again!"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
   logout(request)
   messages.success(request, ("You have been logged out!"))
   return redirect('home')

def register_user(request):
     form = SighUpForm()
    
     if request.method == "POST":
         form = SighUpForm(request.POST)
        
         
         if form.is_valid():
            form.save()
           
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("Registry Successful"))
            return redirect('home')
         
     return render(request, 'register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id = request.user.id)
        user_form = SighUpForm(request.POST or None, request.FILES or None, instance = current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("You have updated your profile!"))
            return redirect('home')

        return render(request, "update_user.html", {'user_form':user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ("Please login first!"))
        return redirect('home')
	  
def twitt_like(request, pk):
	if request.user.is_authenticated:
		twitt = get_object_or_404(Twitt, id=pk)
		if twitt.likes.filter(id=request.user.id):
			twitt.likes.remove(request.user)
		else:
			twitt.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')

def twitt_follow(request, pk):
	if request.user.is_authenticated:
		twitt = get_object_or_404(Twitt, id=pk)
		if twitt.follows.filter(id=request.user.id):
			twitt.follows.remove(request.user)
		else:
			twitt.follows.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
