# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib
import re

import time
from django.core import serializers

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, render_to_response
# from . import models
# from . import models
from FrontSystem import models


# Create your views here.


@login_required()
def index(request):
    return render(request, 'pages/index.html')


@login_required()
def get_index_html(request):
    return render(request, "pages/index.html", locals())


@login_required()
def get_active_html(request):
    return render(request, "pages/active.html", locals())


@login_required()
def get_user_html(request):
    return render(request, "pages/user.html", locals())


@login_required()
def get_order_html(request):
    return render(request, "pages/order.html", locals())


@login_required()
def get_active(request):
    active_obj = models.Active.objects.filter(enabled=True)
    active_list = []
    for i in active_obj:
        active_json = {}
        active_json["id"] = i.id
        active_json["name"] = i.name
        active_json["price"] = i.price
        active_json["start_at"] = i.start_at
        active_json["end_at"] = i.end_at
        active_json["gift"] = i.gift
        active_list.append(active_json)
    return JsonResponse({"data": active_list})


@login_required()
def add_active(request):
    if request.method == "POST":
        active_name = request.POST.get("activeName")
        active_range = request.POST.get("activeRange")
        start = active_range.split(" - ")[0]
        end = active_range.split(" - ")[1]
        active_price = request.POST.get("activePrice")
        active_gift = request.POST.get("activeGift")
        station_num = request.POST.get("stationNum")
        volunteer_num = request.POST.get("volunteerNum")
        group_num = request.POST.get("groupNum")
        try:
            active_obj = models.Active.objects.create(
                name=active_name,
                start_at=start,
                end_at=end,
                price=active_price,
                gift=active_gift
            )
            active_obj.save()
        except Exception as e:
            print e
            return HttpResponse(e)
        if station_num:
            for i in station_num.split(","):
                name = request.POST.get("station[%s]" % i)
                if name:  # station exist
                    try:
                        station_obj = models.Station.objects.create(
                            name=name
                        )
                        station_obj.save()
                        active_obj.station.add(station_obj)
                    except Exception as e:
                        print e
                else:
                    print "This station %s was null or lost." % i
        else:
            print "Station is None"
        if volunteer_num:
            for i in volunteer_num.split(","):
                name = request.POST.get("volunteer[%s]" % i)
                if name:  # volunteer exist
                    try:
                        volunteer_obj = models.Volunteer.objects.create(
                            name=name
                        )
                        volunteer_obj.save()
                        active_obj.volunteer.add(volunteer_obj)
                    except Exception as e:
                        print e
                else:
                    print "This volunteer %s was null or lost." % i
        else:
            print "Volunteer is None"
        if group_num:
            for i in group_num.split(","):
                name = request.POST.get("group[%s]" % i)
                if name:  # group exist
                    try:
                        group_obj = models.Group.objects.create(
                            name=name
                        )
                        group_obj.save()
                        active_obj.group.add(group_obj)
                    except Exception as e:
                        print e
                else:
                    print "This group %s was null or lost." % i
        else:
            print "Group is None"
        return HttpResponse("添加成功")
    else:
        return render_to_response("pages/addActiveForm.html")


def edit_active(request):
    if request.method == "POST":
        id = request.POST.get("active_id")
        active_name = request.POST.get("activeName")
        active_range = request.POST.get("activeRange")
        start = active_range.split(" - ")[0]
        end = active_range.split(" - ")[1]
        active_price = request.POST.get("activePrice")
        active_gift = request.POST.get("activeGift")
        station_num = request.POST.get("stationNum")
        volunteer_num = request.POST.get("volunteerNum")
        group_num = request.POST.get("groupNum")
        active_obj = models.Active.objects.get(id=id)
        if active_obj.name != active_name or \
            active_obj.price != active_price or \
            active_obj.start_at != start or \
            active_obj.end_at != end or \
            active_obj.gift != active_gift:
            active_obj.name = active_name
            active_obj.active_price = active_price
            active_obj.start_at = start
            active_obj.end_at = end
            active_obj.gift = active_gift
            active_obj.save()
        else:
            pass
        if station_num:
            for i in station_num.split(","):
                name = request.POST.get("station[%s]" % i)
                if name:  # station exist
                    try:
                        station_obj = models.Station.objects.create(
                            name=name
                        )
                        station_obj.save()
                        active_obj.station.add(station_obj)
                    except Exception as e:
                        print e
                else:
                    print "This station %s was null or lost." % i
        else:
            print "Station is None"
        if volunteer_num:
            for i in volunteer_num.split(","):
                name = request.POST.get("volunteer[%s]" % i)
                if name:  # volunteer exist
                    try:
                        volunteer_obj = models.Volunteer.objects.create(
                            name=name
                        )
                        volunteer_obj.save()
                        active_obj.volunteer.add(volunteer_obj)
                    except Exception as e:
                        print e
                else:
                    print "This volunteer %s was null or lost." % i
        else:
            print "Volunteer is None"
        if group_num:
            for i in group_num.split(","):
                name = request.POST.get("group[%s]" % i)
                if name:  # group exist
                    try:
                        group_obj = models.Group.objects.create(
                            name=name
                        )
                        group_obj.save()
                        active_obj.group.add(group_obj)
                    except Exception as e:
                        print e
                else:
                    print "This group %s was null or lost." % i
        else:
            print "Group is None"
        return HttpResponse("修改成功")
    else:
        id = request.GET.get("id")
        active_obj = models.Active.objects.get(id=id)
        return render_to_response("pages/editActiveForm.html", locals())


@login_required()
def drop_active(request):
    if request.method == "POST":
        id = request.POST.get("id")
        active_obj = models.Active.objects.get(id=id)
        active_obj.enabled = False
        active_obj.drop_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        active_obj.save()
    return HttpResponse("删除成功！")


@login_required()
def get_classes(request):
    classes_obj = models.Classes.objects.filter(enabled=True)
    classes_list = []
    for i in classes_obj:
        class_json = {}
        class_json["id"] = i.id
        class_json["name"] = i.name
        class_json["price"] = i.price
        class_json["qr"] = i.qr.id
        class_json["qr_path"] = str(i.qr.file)
        # print i.qr,type(i.qr)
        classes_list.append(class_json)
    return JsonResponse({"data": classes_list})


@login_required()
def get_apply(request):
    apply_obj = models.ApplyForm.objects.filter(enabled=True)
    apply_list = []
    for i in apply_obj:
        apply_json = {}
        apply_json["name"] = i.name
        apply_json["phone"] = i.phone
        apply_json["sex"] = i.get_sex_display()
        apply_json["create_at"] = i.create_at
        apply_json["classes"] = models.Classes.objects.get(id=i.classes_id).name
        apply_json["portrait"] = str(i.portrait)
        # print i.qr,type(i.qr)
        apply_list.append(apply_json)
    return JsonResponse({"data": apply_list})


@login_required()
def set_classes(request):
    if request.method == "POST":
        my_post = urllib.unquote(request.body)
        action = request.POST.get('action')
        if action == "upload":
            try:
                qr_obj = models.Qr.objects.create(
                    file=request.FILES["upload"]
                )
                qr_obj.save()
                return JsonResponse({"data": [], "upload": {"id": qr_obj.id}})
            except Exception as e:
                print "upload file fail, ", e
                return JsonResponse({"data": [], "fileErrors": {"name": "Error", "status": e}})
        id = re.findall(r"&data\[(\d*?)]\[name]", my_post)[0]
        # id = request.POST.get('data[0][id]')
        name = request.POST.get('data[' + id + '][name]')
        price = request.POST.get('data[' + id + '][price]')
        qr = request.POST.get('data[' + id + '][qr]')
        print action
        print my_post
        if action == "create":
            try:
                classes_obj = models.Classes.objects.create(
                    name=name,
                    price=price,
                    qr=models.Qr.objects.get(id=qr),
                    enabled=True
                )
                classes_obj.save()
                return JsonResponse({"data": [{"id": classes_obj.id,
                                               "name": classes_obj.name,
                                               "price": classes_obj.price,
                                               "qr_path": str(classes_obj.qr.file),
                                               "qr": classes_obj.qr.id}]})
            except Exception as e:
                print "create classes fail, ", e
                return JsonResponse({"data": []})
        if action == "edit":
            try:
                classes_obj = models.Classes.objects.get(id=id)
                classes_obj.name = name
                classes_obj.price = price
                classes_obj.qr = models.Qr.objects.get(id=qr)
                classes_obj.save()
                return JsonResponse({"data": [{"id": classes_obj.id,
                                               "name": classes_obj.name,
                                               "price": classes_obj.price,
                                               "qr_path": str(classes_obj.qr.file),
                                               "qr": classes_obj.qr.id}]})
            except Exception as e:
                print "edit classes fail, ", e
                return JsonResponse({"data": []})
        if action == "remove":
            try:
                classes_obj = models.Classes.objects.get(id=id)
                classes_obj.enabled = False
                classes_obj.save()
                return get_classes(request)
            except Exception as e:
                print "delete classes fail, ", e
                return JsonResponse({"data": []})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username, password
        user = auth.authenticate(username=username, password=password)
        print "user", user
        if user is not None:
            try:
                auth.login(request, user)
                request.session.set_expiry(60 * 60 * 24 * 7)
                print 'session expires at :', request.session.get_expiry_date()
                # test_type_list = models.TestType.objects.all()
                return HttpResponseRedirect('/index/')
            except ObjectDoesNotExist:
                return render(request, 'pages/login.html',
                              {'login_err': u"Account not exist ! Pls retry or contact administrator!!"})
        else:
            return render(request, 'pages/login.html', {'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'pages/login.html')

