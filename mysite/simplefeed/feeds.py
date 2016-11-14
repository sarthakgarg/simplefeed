from django.contrib.syndication.views import Feed
from django.urls import reverse
from simplefeed.models import Target, Hash
from django.contrib.auth.models import Group, User

class TargetFeed(Feed):
    title = "Url changes"
    link = "/feed/rss/"
    description = "Updates on the changes to your urls"
    def get_object(self, request, user_id):
        print user_id
        p = Hash.objects.get(hash = user_id)
        return p.owner

    def item_title(self, item):
        if item.diff == "":
            return item.url + ": new link"
        else:
            return item.url + item.diff

    def item_description(self, item):
        return item.diff

    def item_link(self, item):
        return reverse('index')

    def items(self, item):
        return Target.objects.filter(owner = item).order_by('-epoch')
