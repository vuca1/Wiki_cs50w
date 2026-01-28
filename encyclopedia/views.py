import re
import random

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    """
    Homepage
    Renders all entries/titles in a list.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    """
    Renders 'title' Wiki page.
    
    :param title: title of a page
    """
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "entry": util.get_entry(title)
    })

def search(request):
    """
    Uses form to search through all entries.
    When found perfect match it opens the found page.
    When found substring it shows list with all substrings.
    """
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

def new_page(request):
    """
    Renders new page if entered by GET method.
    If entered by POST creates new Wiki page according to the form.
    """
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST["title"]
        content = request.POST["content"]

        if title in entries:
            return render(request, "encyclopedia/new_page.html", {
                "message": f"Page for {title} already exists."
            })
        elif title and content:
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(reverse("title", args=(title,)))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "message": "Something went wrong. Try again."
            })
        
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    """
    
    """
    if request.method == "POST":
        new_content = request.POST["content"]
        util.save_entry(title, new_content)
        messages.success(request, f"Page '{title}' was updated successfully.")
        return HttpResponseRedirect(reverse("title", args=(title,)))

    old_content = util.get_entry(title=title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": old_content,
    })

def random_page(request):
    """
    Render random page from all entries.
    """
    entries = util.list_entries()
    entry = entries[random.randint(0, (len(entries) - 1))]

    return HttpResponseRedirect(reverse("title", args=(entry,)))