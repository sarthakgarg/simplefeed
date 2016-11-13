from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Target
from django.template import loader
import json
import urllib, re
from bs4 import BeautifulSoup
from difflib import Differ

def diff(a, b):
    l1 = a.split(' ')
    l2 = b.split(' ')
    dif = list(Differ().compare(l1, l2))
    return " ".join(['<b>'+i[2:]+'</b>' if i[:1] == '+' else i[2:] for i in dif if not i[:1] in '-?'])

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title','spanid','button']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    return True

def parsehtml(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    s = ''.join(visible_texts)
    s = ''.join(s.split())
    return s

def index(request):
    target_list = Target.objects.order_by('url').all()
    for t in target_list:
        print t.url
        curr = parsehtml(t.url)
        if curr != t.content:
            t.diff = diff(curr, t.content)
            t.content = curr
        else:
            t.diff = ""
        t.save()
    template = loader.get_template('simplefeed/index.html')
    context = {
        'target_list': target_list,
    }
    return HttpResponse(template.render(context, request))


def addform(request):
    template = loader.get_template('simplefeed/addform.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def add(request):

    q = Target(url = request.POST['url'], category = request.POST['category'], content = parsehtml(request.POST['url']))
    q.save()
    return HttpResponseRedirect('/feed/')

def updateform(request, target_id):
    template = loader.get_template('simplefeed/updateform.html')
    q = Target.objects.get(pk = target_id)
    context = {
        'target': q,
    }
    return HttpResponse(template.render(context, request))

def update(request, target_id):
    q = Target.objects.get(pk = target_id)
    q.url = request.POST['url']
    q.category = request.POST['category']
#    q.content = parsehtml(request.POST['url'])
    q.save()
    return HttpResponseRedirect("/feed/")

def delete(request, target_id):
    q = Target.objects.get(pk = target_id)
    q.delete()
    return HttpResponseRedirect("/feed/")


#def serve(request):
#    fruit_list = [fruit.as_json() for fruit in Fruits.objects.order_by('fruit_name').all()]
#    return HttpResponse(json.dumps(fruit_list), content_type = 'application/json')
