from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user.views import watcher_home, coordinator_home, manager_home

def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)


def error_500(request):
        data = {}
        return render(request,'500.html', data)


@login_required
def home(request):
    '''Wildlife watcher home page. '''
    role = request.user.role
    if 2 == role:
        return redirect(watcher_home)
    if 3 == role:
        return redirect(coordinator_home)
    if 4 == role:
        return redirect(manager_home)
    return render(request, 'backend/home.html')


@login_required
def help(request):
    '''Help page. '''
    return render(request, 'backend/help.html')

def project(request):
    '''Project information page. '''
    return render(request, 'backend/project.html')

def conservation_booklet(request):
    '''Conservation booklet page. '''
    return render(request, 'backend/conservation_booklet.html')
