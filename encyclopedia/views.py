from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
import random

from . import util

markdowner = Markdown()

class NewContentForm(forms.Form):        
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input'}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea', 'rows': '5', 'cols': '20'}), label="New Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, title):
    content = util.get_entry(title)
    entry = {"title": title, "content": markdowner.convert(content)}
    return render(request, "encyclopedia/wiki.html", {
        "entry": entry
    })

def search(request):
    query = request.GET.get('q').capitalize()
    entries = util.list_entries()
    resultList = []

    entriesUpper = [entry.upper() for entry in entries]

    for entry in entriesUpper:
        if query.upper() == entry:
            return HttpResponseRedirect(f"wiki/{query}")
        if query.upper() in entry:
            resultList.append(entry)
            return render(request, "encyclopedia/search.html",{
                "entries":resultList
            })

    if query.upper() not in entriesUpper:
        return HttpResponseRedirect(f"wiki/{query}")

def add(request):
    if request.method == "POST":
        form = NewContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                render(request, "encyclopedia/add.html")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "add.html",{
                "form": form
            })
    return render(request, "encyclopedia/add.html",{
        "form": NewContentForm()
    })

def edit(request, title):
    form = NewContentForm(initial={'title': title, 'content': util.get_entry(title)})
    if request.method == "POST":
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": form
            })

def random_page(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    content = util.get_entry(selected_page)
    entry = {"title": selected_page, "content": markdowner.convert(content)}
    return render(request, "encyclopedia/wiki.html", {
        "entry": entry
    })

