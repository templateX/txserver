from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import uuid
import requests
import json

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def github_connect(request):
    url = f'https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CONNECT_ID}&redirect_uri={settings.REDIRECT_URI}&state={uuid.uuid4().hex}'
    print(url)
    return redirect(url)

def github_connect_callback(request):
    code = request.GET['code']
    query = {
        'client_id': settings.GITHUB_CONNECT_ID,
        'client_secret': settings.GITHUB_CONNECT_SECRET,
        'code': code,
        'redirect_uri': settings.REDIRECT_URI
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', params=query, headers=headers)
    data = response.json()
    access_token = data['access_token']
    return redirect('github_projects', access_token=access_token)

def github_projects(request, access_token):
    print(access_token)
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    data = response.json()
    print(data)
    repo_link = data['repos_url']
    response = requests.get(repo_link, headers=headers)
    repos = response.json()
    context = {
        'repos': repos
    }
    return render(request, 'home/projects.html', context)
