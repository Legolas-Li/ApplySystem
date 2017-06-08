# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
#from . import models
#from . import models
from FrontSystem import models
# Create your views here.


@login_required()
def index(request):
    # return HttpResponse("Hello, world. You're at the home index.")
    # username = request.COOKIES.get('username', '')
    return render(request, 'pages/index.html')


@login_required()
def get_index_html(request):
    return render(request,"pages/index.html",locals())


@login_required()
def get_front_design_html(request):
    if request.method == "POST":
        title = request.POST.get("title")
        start = request.POST.get("start")
        end = request.POST.get("end")
        address = request.POST.get("address")
        description = request.POST.get("descriptions")
        print locals()
        try:
            project_obj = models.Project.objects.get(id=1)
            project_obj.title = title
            project_obj.start = start
            project_obj.end = end
            project_obj.address = address
            project_obj.description = description
            project_obj.save()
            return HttpResponse(u"修改成功")
        except Exception as e:
            print e
            return HttpResponse(e)
    else:
        project = models.Project.objects.get(id=1)
        return render(request,"pages/design.html",locals())


@login_required()
def get_tables_html(request):
    return render(request,"pages/tables.html",locals())


@login_required()
def get_classes(request):
    classes_obj = models.Classes.objects.filter(enabled=True)
    classes_list = []
    for i in classes_obj:
        class_json = {}
        class_json["name"]=i.name
        class_json["price"]=i.price
        class_json["qr"]=str(i.qr)
        #print i.qr,type(i.qr)
        classes_list.append(class_json)
    return JsonResponse({"data": classes_list})


@login_required()
def get_apply(request):
    apply_obj = models.ApplyForm.objects.filter(enabled=True)
    apply_list = []
    for i in apply_obj:
        apply_json = {}
        apply_json["name"]=i.name
        apply_json["phone"]=i.phone
        apply_json["sex"]=i.sex
        apply_json["classes"]=models.Classes.objects.get(id=i.classes_id).name
        apply_json["portrait"]=str(i.portrait)
        #print i.qr,type(i.qr)
        apply_list.append(apply_json)
    return JsonResponse({"data": apply_list})


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

