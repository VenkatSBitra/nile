from django.shortcuts import render, redirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}! Please Sign In now.')
            return redirect("/login")
        else:
            messages.error(request, "Account creation failed. Please check the warnings and update.")
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {"form":form})

@login_required
def profile(request):
    if request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account has been updated.')
            return redirect("/profile")
        else:
            messages.error(request, 'Account could not be updated.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'main/profile.html', context)

