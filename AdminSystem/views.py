# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


@login_required()
def index(request):
    # return HttpResponse("Hello, world. You're at the home index.")
    # username = request.COOKIES.get('username', '')
    return render(request, 'pages/index.html')


def get_index_html(request):
    return render(request,"pages/index.html",locals())


def get_front_design_html(request):
    return render(request,"pages/design.html",locals())


def get_tables_html(request):
    return render(request,"pages/tables.html",locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username,password
        user = auth.authenticate(username=username, password=password)
        print "user",user
        if user is not None:
            try:
                auth.login(request, user)
                request.session.set_expiry(60 * 60 * 24 * 7)
                print 'session expires at :',request.session.get_expiry_date()
                # test_type_list = models.TestType.objects.all()
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return render(request, 'pages/login.html',
                              {'login_err': u"Account not exist ! Pls retry or contact administrator!!"})
        else:
            return render(request, 'pages/login.html', {'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'pages/login.html')
