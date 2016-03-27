from django.conf.urls import url

from . import views

urlpatterns = [
	#Home Page
	url(r'^$', views.index, name='index'),
	#Show all topics
	url(r'^topics/$', views.topics, name='topics'),
	#Edit a topic -----
	url(r'^edit_topic/(?P<topic_id>\d+)/$', views.edit_topic, name='edit_topic'),
	#Detail for single topic
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
	#Page to add new topic
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
	#Adding a new entry
	url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
	#Page for editing entries
	url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]