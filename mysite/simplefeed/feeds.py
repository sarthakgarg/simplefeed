from django.contrib.syndication.views import Feed
from django.urls import reverse
from simplefeed.models import Target

class TargetFeed(Feed):
    title = "Url changes"
    link = "/feed/rss/"
    description = "Updates on the changes to your urls"
    def items(self):
        return Target.objects.order_by('-epoch')

    def item_title(self, item):
        if item.diff == "":
            return item.url + ": new link"
        else:
            return item.url + item.diff

    def item_description(self, item):
        return item.diff

    def item_link(self, item):
        return reverse('index')
