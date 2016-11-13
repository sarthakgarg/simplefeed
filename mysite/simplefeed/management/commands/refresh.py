from django.core.management.base import BaseCommand, CommandError
from simplefeed.models import Target
import urllib, re
from lxml.html.diff import htmldiff
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


class Command(BaseCommand):
    def handle(self, *args, **options):
        target_list = Target.objects.all();
        for t in target_list:
            print t.content
            curr = gethtml(t.url)
            print curr
            if(curr != t.content):
                t.diff = diff(t.content, curr)
                t.content = curr
                t.save()
