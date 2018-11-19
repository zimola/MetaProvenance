from django.shortcuts import render
from .forms import SignInForm, SignUpForm


def account_signup(request):
    form = SignUpForm(request.POST or None)
    action = 'SignUp'

    if request.method == 'POST' and form.is_valid():
        # todo clean password
        #user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # print(email, password)
        pass

    return render(request, 'accounts/signup.html', context={'form': form, 'action': action})


def account_signin(request):
    form = SignInForm(request.POST or None)
    action = 'SignIn'

    if request.method == 'POST' and form.is_valid():
        #user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # print(email, password)
        pass

    return render(request, 'accounts/signin.html', context={'form': form, 'action': action})



def account_logout(request):
    pass


def account_edit(request):
    pass