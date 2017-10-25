'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from ribbit_app.forms import AuthenticateForm, UserCreateForm, RibbitForm
from ribbit_app.models import Ribbit

# Create your views here.
def index(request,auth_form=None,user_form=None):
	if request.user.is_authenticated():
		ribbit_form = RibbitForm()
		user = request.user
		ribbits_self = Ribbit.objects.filter(user=user.id)
		ribbits_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all)
		ribbits = ribbits_self | ribbits_buddies
		return render(request,
						'buddies.html',
						{'ribbit_form':ribbit_form,'user':user,
						'ribbits':ribbits,
						'next_url':'/',})
	else:
		auth_form = auth_form or AuthenticateForm()
		user_form = user_form or UserCreateForm()

		return render(request,
						'home.html',
						{'auth_form':auth_form,'user_form':user_form,})

def login_view(request):
	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		print "Heyy"
		if form.is_valid():
			print "Hellooo"
			login(request,form.get_user())
			return redirect('/')
		else:
			return index(request,auth_form=form)
	return redirect('/')

def logout_view(request):
	logout(request)
	return redirect('/')

def signup(request):
	user_form = UserCreateForm(data=request.POST)
	if request.method == 'POST':
		print "Hi there"
		if user_form.is_valid():
			print "Hello"
			username = user_form.clean_username()
			password = user_form.clean_password2()
			user_form.save()

			user=authenticate(username=username,password=password)
			login(request,user)
			return redirect('/')
		else:
			return index(request,user_form=user_form)
	return redirect('/')
'''
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from ribbit_app.forms import AuthenticateForm, UserCreateForm, RibbitForm
from ribbit_app.models import Ribbit


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        ribbit_form = RibbitForm()
        user = request.user
        ribbits_self = Ribbit.objects.filter(user=user.id)
        ribbits_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all)
        ribbits = ribbits_self | ribbits_buddies

        return render(request,
                      'buddies.html',
                      {'ribbit_form': ribbit_form, 'user': user,
                       'ribbits': ribbits,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        print "hii"
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            print "heyy"
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        print "hello"
    	if user_form.is_valid():
    	    print "hi"
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')

