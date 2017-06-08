# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib
import re

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
        play_range = request.POST.get("playRange")
        start = play_range.split(" - ")[0]
        end = play_range.split(" - ")[1]
        address = request.POST.get("address")
        description = request.POST.get("descriptions")
        print locals()
        try:
            project_obj = models.Project.objects.create(
                title = title,
                start_at = start,
                end_at = end,
                address = address,
                description = description
            )
            project_obj.save()
            return HttpResponse(u"修改成功")
        except Exception as e:
            print e
            return HttpResponse(e)
    else:
        try:
            project = models.Project.objects.order_by("id")[::-1][0]
        except Exception as e:
            project = None
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
        class_json["id"]=i.id
        class_json["name"]=i.name
        class_json["price"]=i.price
        class_json["qr"]=i.qr.id
        class_json["qr_path"]=str(i.qr.file)
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


@login_required()
def set_classes(request):
    if request.method == "POST":
        my_post = urllib.unquote(request.body)
        action = request.POST.get('action')
        if action == "upload":
            try:
                qr_obj=models.Qr.objects.create(
                    file=request.FILES["upload"]
                )
                qr_obj.save()
                return JsonResponse({"data":[],"upload":{"id":qr_obj.id}})
            except Exception as e:
                print "upload file fail, ",e
                return JsonResponse({"data":[],"fileErrors":{"name":"Error","status": e}})
        id = re.findall(r"&data\[(\d*?)]\[name]",my_post)[0]
        #id = request.POST.get('data[0][id]')
        name = request.POST.get('data['+id+'][name]')
        price = request.POST.get('data['+id+'][price]')
        qr = request.POST.get('data['+id+'][qr]')
        print action
        print my_post
        if action == "create":
            try:
                classes_obj=models.Classes.objects.create(
                    name=name,
                    price=price,
                    qr=models.Qr.objects.get(id=qr),
                    enabled=True
                )
                classes_obj.save()
                return JsonResponse({"data":[{"id":classes_obj.id,
                                               "name":classes_obj.name,
                                               "price":classes_obj.price,
                                               "qr_path":str(classes_obj.qr.file),
                                               "qr":classes_obj.qr.id}]})
            except Exception as e:
                print "create classes fail, ",e
                return JsonResponse({"data":[]})
        if action == "edit":
            try:
                classes_obj=models.Classes.objects.get(id=id)
                classes_obj.name=name
                classes_obj.price=price
                classes_obj.qr=models.Qr.objects.get(id=qr)
                classes_obj.save()
                return JsonResponse({"data":[{"id":classes_obj.id,
                                             "name":classes_obj.name,
                                             "price":classes_obj.price,
                                             "qr_path":str(classes_obj.qr.file),
                                             "qr":classes_obj.qr.id}]})
            except Exception as e:
                print "edit classes fail, ",e
                return JsonResponse({"data":[]})
        if action == "remove":
            try:
                classes_obj=models.Classes.objects.get(id=id)
                classes_obj.enabled=False
                classes_obj.save()     
                return get_classes(request)
            except Exception as e:
                print "delete classes fail, ",e
                return JsonResponse({"data":[]})

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

