from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""The homepage for learning log"""
	return render(request, 'practises/index.html')

@login_required
def topics(request):
	"""Shows all topics"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'practises/topics.html', context)

@login_required
def topic(request, topic_id):
	"""Shows all topics"""
	topic = Topic.objects.get(id=topic_id)
	#Make sure the topic belongs to the current user
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'practises/topic.html', context)

@login_required
def new_topic(request):
	"""Add a new topic"""
	if request.method != 'POST':
		#No data submitted, submit a blank form
		form = TopicForm()
	else:
		#POST data submitted, process data
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('practises:topics'))

	context = {'form': form}
	return render(request, 'practises/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	#Add new entry for a particular topic
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		#No data submitted, submit a blank form
		form = EntryForm()
	else:
		#POST data submitted, process data
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('practises:topic', args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'practises/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edit an existing entry"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic   #Didnt write this line for my edit topic view
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#Initial request; pre-fill form with the current entry
		form = EntryForm(instance=entry)
	else:
		#POST data submitted, submit data
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('practises:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'practises/edit_entry.html', context)

@login_required
def edit_topic(request, topic_id):
	"""Edit an existing topic"""
	topic = Topic.objects.get(id=topic_id)
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#No data submitted, submit a blank form
		form = TopicForm(instance=topic)
	else:
		#POST dat submitted, submit data
		form = TopicForm(instance=topic, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('practises:topic', args=[topic.id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'practises/edit_topic.html', context)

	
	

