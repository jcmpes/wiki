from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    context = {
        "title": title,
        "entry": util.get_entry(title)
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