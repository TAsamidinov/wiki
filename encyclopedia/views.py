from django.shortcuts import render
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry (request, title):
    entry_content = util.get_entry(title)

    if (entry_content is None):
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })
    else:
        content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def search (request):
    query = request.GET.get("q", "")
    entry_content = util.get_entry(query)
    entries = util.list_entries()

    if (entry_content is None):
        
        return render(request, "encyclopedia/results.html", {
            "entries": [entry for entry in entries if query in entry],
            "query": query,
        })
    else:
        content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": content
        })    

def new_page (request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists."
            })

        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    return render (request, "encyclopedia/new_page.html")

def edit_page (request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    
    return entry(request, random_title)