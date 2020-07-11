from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "titles": util.list_entries()
    })


def entry(request, title):
    md = markdown.Markdown()
    md_entry = md.convert(util.get_entry(title))
    context = {
        "title": title,
        "entry": md_entry
    }
    return render(request, "encyclopedia/entry.html", context)


def search(request):
    query = request.GET.get('q')
    if util.get_entry(query) != None:
        context = {
        "title": query,
        "entry": util.get_entry(query)
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query in entry:
                results.append(entry)
        context = {
            "results": results
        }
        return render(request, "encyclopedia/search.html", context)


def new(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        entries = util.list_entries()
        for item in entries:
            if item == title:
                messages.add_message(request, messages.ERROR, 'Entry already exists.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=(title,)))
                
    else:
        return render(request, "encyclopedia/new.html")

def edit(request, title):
    if request.method == "POST":
        if request.POST['title'] != '':
            title = request.POST['title']
        else:
            title = title
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=(title,)))
    else:

        entry = util.get_entry(title)
        context = {
            "title": title,
            "entry": entry
        }
        return render(request, 'encyclopedia/edit.html', context)