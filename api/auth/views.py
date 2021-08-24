from django.http import HttpResponse
from django.shortcuts import redirect

def github_login(request):
    url = 'https://github.com/login/oauth/authorize'
    return redirect(url)

def github_callback(request):
    print(request.GET['code'])
    return HttpResponse('Done')
