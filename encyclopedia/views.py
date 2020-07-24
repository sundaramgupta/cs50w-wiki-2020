from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from markdown2 import markdown
from random import randint
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
	content=util.get_entry(title)
	if not content:
		content="this does not exist"

	#converting markdown to html
	content=markdown(content)

	return render(request, "encyclopedia/entry.html",{
		"title":title,
		"content":content
		})

def create(request):
	if request.method =='POST':

		#title given by the user
		title=request.POST.get('title')

		#content given by the user
		content=request.POST.get('content')

		if not title or not content:
			return render(request,"encyclopedia/create.html", {
				"message": "Title or Content is missing. Please provide both."
				})
		if title in util.list_entries():
				return render(request,"encyclopedia/create.html", {
				"message": "Title is already feeded."
				})

		#save both content and title
		util.save_entry(title, content)

		#redirect to the entry page after saving the new page
		return redirect("entry", title=title)

	return render(request, "encyclopedia/create.html")

def search(request):
	query=request.GET.get('q')
	if query in util.list_entries():

		#if searched keyword present as a title, redirects to that page
		return HttpResponseRedirect("wiki/"+query)
	else:

		#creating a list to store substring
		substring=[]
		for post in util.list_entries():

			#if keyword is in the title append the title to the list
			if query in post:
				substring.append(post)

		#render index.html passing the title containing the substrings
		return render(request, "encyclopedia/index.html",{
			"entries": substring
			})

def edit(request, title):
	content=util.get_entry(title)
	if request.method=='POST':

		#getting the new content edited by the user
		content = request.POST.get("content")

		#getting the new title edited by the user
		title=request.POST.get("title")

		#saving new content and title
		util.save_entry(title, content)

		#redirect to the edited page
		return redirect("entry", title=title)

	return render(request, "encyclopedia/edit.html",{
		"title": title,
		"content": content
		})

def random(request):
	entries=util.list_entries()

	#randint is generating a random number between 0 and len(entries)-1
	#rand_entry is storing the value of the element present at that index of the list 
	rand_entry = entries[randint(0, len(entries)-1)]

	#redirecting to the random page
	return redirect('entry', title=rand_entry)

