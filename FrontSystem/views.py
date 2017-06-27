# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from FrontSystem.models import ApplyForm
from . import models
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic

conf = WechatConf(
    token='legolasli', 
    appid='wx6970d980f274d1de', 
    appsecret='08ee9882234c7553c038c452c6a74d24', 
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='J3V0OHUxpRxfpffQFhTqBMzOoDFJN56wP4U5BydnIMn'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)

def get_wx_accept(request):
    if request.method == "GET":
        signature = request.GET.get("signature")
        timestamp = request.GET.get("timestamp")
        nonce = request.GET.get("nonce")
        echostr = request.GET.get("echostr")
        print "nonce", nonce
        if wechat.check_signature(signature, timestamp, nonce):
            print 'Accept'
            return HttpResponse(echostr)
        else:
            print 'Wrong'
            return HttpResponse('Wrong')
    else:
        try:
            wechat.parse_data(request.body)
        except ParseError:
            print 'Invalid Body Text'
        id = wechat.message.id          # 对应于 XML 中的 MsgId
        target = wechat.message.target  # 对应于 XML 中的 ToUserName
        source = wechat.message.source  # 对应于 XML 中的 FromUserName
        time = wechat.message.time      # 对应于 XML 中的 CreateTime
        type = wechat.message.type      # 对应于 XML 中的 MsgType
        raw = wechat.message.raw        # 原始 XML 文本，方便进行其他分析
        xml = wechat.response_text(content='文本回复')
        return HttpResponse(xml)
	

# Create your views here.
def get_apply_html(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        sex = request.POST.get("sex")
        classes_id = request.POST.get("classes")
        try:
            portrait=request.FILES['portrait']
        except Exception as e:
            print "Portrait lost", e
            portrait=None
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
        return render(request, "result.html",{"msg":"报名成功,请长按二维码缴费","status":"succeed", "qr":models.Classes.objects.get(id=classes_id).qr.file})
    else:
        classes = models.Classes.objects.filter(enabled=True)
        try:
            project = models.Project.objects.order_by("id")[::-1][0]
        except Exception as e:
            print e
            project = None
        # description = "教育部指定的上海市xxx招生考试网上报名入口;信息内容以网报指南和网报日程的发布为主"
        return render(request,'apply.html',locals())
