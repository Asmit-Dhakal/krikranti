from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Contact, Profile


# Create your views here
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome "{username}" your account created')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profilepage(request):
    return render(request, 'users/profile.html', )


def profileupdate(request, user):
    profile = Profile.objects.values(user=user)
    pform = ProfileForm(request.POST or None, instance=profile)

    if pform.is_valid():
        pform.save()
        return redirect('profile')
    return render(request, 'users/profile-form.html', {'pform': pform})


def handlelogout(request):
    logout(request)
    messages.success(request, f'Logout Successfully')
    return redirect('shop/index')
