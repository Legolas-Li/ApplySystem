# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from FrontSystem.models import ApplyForm
from . import models

# Create your views here.
def get_apply_html(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        sex = request.POST.get("sex")
        classes_id = request.POST.get("classes")
        portrait=request.FILES['portrait']
        print locals()
        try:
            apply_form_obj = models.ApplyForm.objects.create(
                name=name,
                phone=phone,
                sex=sex,
                classes=models.Classes.objects.get(id=classes_id),
                portrait=portrait
            )
        except Exception as e:
            print "Create form fail: %s " % e
            return render(request, "result.html", {"msg": "报名失败, %s" % e,"status":"failed", "qr": None})
        return render(request, "result.html",{"msg":"报名成功,请长按二维码缴费","status":"succeed", "qr":models.Classes.objects.get(id=classes_id).qr})
    else:
        classes = models.Classes.objects.filter(enabled=True)
        try:
            project = models.Project.objects.get(id=1)
        except Exception as e:
            print e
            project = None
        # description = "教育部指定的上海市xxx招生考试网上报名入口;信息内容以网报指南和网报日程的发布为主"
        return render(request,'apply.html',locals())