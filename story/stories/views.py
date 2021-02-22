import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html")

def stories_list_view(request, *args, **kwargs):
    return render(request, "stories/list.html")

def stories_detail_view(request, story_id, *args, **kwargs):
    return render(request, "stories/detail.html", context={"story_id": story_id})
