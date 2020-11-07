from django.db import models


News = "News"
Events = "Events"

POSTED_AS = (
    (News, "News"),
    (Events, "Events")
)


class NewsAndEvent(models.Model):
    title = models.CharField(max_length=120, null=True)
    summary = models.TextField(blank=True)
    posted_as = models.TextField(choices=POSTED_AS, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    email = models.EmailField(null=True, blank=True)
    # subject = models.CharField(max_length=120, null=True)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
