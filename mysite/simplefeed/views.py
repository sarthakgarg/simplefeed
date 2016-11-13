from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Target
from django.template import loader
import json
import urllib, re
from bs4 import BeautifulSoup
import difflib
from lxml.html.diff import htmldiff

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
    html = urllib.urlopen(url).read()
    return html

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
    #visible_texts = visible_texts[:-51]
    s = ''.join(visible_texts)
    s = ''.join(s.split())
    return s

def index(request):
    target_list = Target.objects.order_by('url').all()
    for t in target_list:
        curr = gethtml(t.url)
        if curr != t.content:
            t.diff = diff(t.content, curr)
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
   # q.content = parsehtml(request.POST['url'])
    q.content = ""
    q.save()
    return HttpResponseRedirect("/feed/")

def delete(request, target_id):
    q = Target.objects.get(pk = target_id)
    q.delete()
    return HttpResponseRedirect("/feed/")


#def serve(request):
#    fruit_list = [fruit.as_json() for fruit in Fruits.objects.order_by('fruit_name').all()]
#    return HttpResponse(json.dumps(fruit_list), content_type = 'application/json')
