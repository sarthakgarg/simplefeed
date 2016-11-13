from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Target
from django.template import loader
import json
import urllib, re
from bs4 import BeautifulSoup
import difflib
from lxml.html.diff import htmldiff
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
import ssl

def diff(h1, h2):
    print h1
    print h2
    a = htmldiff(h1, h2)
    start = []
    end = []
    n = len(a);
    for i in range(n-6):
        if a[i:i+6] == "</ins>":
            end.append(i);
        if a[i:i+5] == "<ins>":
            start.append(i);
    res = ""
    for (x, y) in zip(start, end):
        res += a[x+5:y]
    return res

def gethtml(url):
    context = ssl._create_unverified_context()
    html = urllib.urlopen(url, context = context).read()
    return html


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    target_list = Target.objects.filter(owner=request.user).order_by('url')
    template = loader.get_template('simplefeed/index.html')
    context = {
        'target_list': target_list,
    }
    return HttpResponse(template.render(context, request))

def register_show(request):
    template = loader.get_template('simplefeed/register.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if len(User.objects.filter(username = request.POST['username'])) > 0:
        return HttpResponse("User already exists")
    else:
        User.objects.create_user(username = request.POST['username'], password = request.POST['password'])
        return HttpResponseRedirect('/feed/')

def login_show(request):
    template = loader.get_template('simplefeed/login.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def loginuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/feed')
            # Redirect to a success page.
        else:
            return HttpResponse("Disabled account")
            # Return a 'disabled account' error message

    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect('/feed/login_show')

def logoutuser(request):
    logout(request)
    return HttpResponseRedirect('/feed/')

def addform(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    template = loader.get_template('simplefeed/addform.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    q = Target(url = request.POST['url'], category = request.POST['category'], content = gethtml(request.POST['url']), owner = request.user)
    q.save()
    return HttpResponseRedirect('/feed/')

def updateform(request, target_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    template = loader.get_template('simplefeed/updateform.html')
    q = Target.objects.get(pk = target_id, owner = request.user)
    context = {
        'target': q,
    }
    return HttpResponse(template.render(context, request))

def update(request, target_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    q = Target.objects.get(pk = target_id)
    q.url = request.POST['url']
    q.category = request.POST['category']
    q.content = gethtml(request.POST['url'])
    q.diff = ""
    q.save()
    return HttpResponseRedirect("/feed/")

def delete(request, target_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/feed/login_show')
    q = Target.objects.get(pk = target_id)
    q.delete()
    return HttpResponseRedirect("/feed/")
