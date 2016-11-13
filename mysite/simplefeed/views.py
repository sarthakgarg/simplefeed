from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Target
from django.template import loader
import json
import urllib, re
from bs4 import BeautifulSoup

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
    q.content = parsehtml(request.POST['url'])
    q.save()
    return HttpResponseRedirect("/feed/")

def delete(request, target_id):
    q = Target.objects.get(pk = target_id)
    q.delete()
    return HttpResponseRedirect("/feed/")


#def serve(request):
#    fruit_list = [fruit.as_json() for fruit in Fruits.objects.order_by('fruit_name').all()]
#    return HttpResponse(json.dumps(fruit_list), content_type = 'application/json')
