import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "entry": util.get_entry(title)
    })

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q")

    for entry in entries:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse("title", args=(entry,)))
        
    finds = []
    for entry in entries:
        if query.lower() in entry.lower():
            finds.append(entry)

    return render(request, "encyclopedia/index.html", {
        "entries": finds,
        "query": query
    })
