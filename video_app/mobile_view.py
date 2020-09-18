from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def m_video(request):
    return render(request, 'm-list.html', {})


def userlist(request):
    return render(request, 'userListPanel.html')

def userdetail(request):
    return render(request, 'userDetail.html')

def userlogin(request):
    if request.method == 'GET':
        return render(request, 'userListPanelLogin.html')
    if request.method == 'POST':
        context = {}
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to='userlist')
        else:
            errormessage="Login Error"
            context['errormessage']=errormessage
        return render(request, 'userListPanelLogin.html', context=context)