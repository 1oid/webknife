# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View
import socket
from urlparse import urlparse
from .models import MyShellModels, UserModels
from loknife.test import *
from django.http import JsonResponse

def gethostipbyname(url):
    host = urlparse(url).netloc
    try:
        return socket.gethostbyname(host)
    except:
        return "NO IP"

def GetModelsById(request,id):
    userinfo = reqSession(request)
    if userinfo:
        try:
            return userinfo.myshellmodels_set.get(pk=id)
        except:
            return False

def reqSession(request):
    if request.session.has_key('User_ID'):
        return UserModels.objects.get(id=request.session['User_ID'])

# 首页视图
class Index(View):

    def get(self, request):
        userinfo = reqSession(request)
        if userinfo:
            obj = userinfo.myshellmodels_set.all()
            return render(request, "knifeindex.html", {"alltasks": obj, "userinfo": userinfo})
        return redirect('/knife/login/')

# 添加shell
class Add(View):

    def get(self, request):
        userinfo = reqSession(request)
        return render(request, "addtask.html", {"userinfo": userinfo})

    def post(self, request):
        if request.POST:
            userinfo = reqSession(request)
            target, password, script, mark = request.POST['target'], request.POST['password'], request.POST['script'], request.POST['mark']
            ip = gethostipbyname(target)
            if userinfo:
                userinfo.myshellmodels_set.create(target=target, password=password, script=script, ip=ip, mark=mark).save()
                return redirect('/knife/')
            return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

class Edit(View):

    def get(self, request, **kwargs):
        userinfo = reqSession(request)
        taskid = int(kwargs['taskid'])
        obj = GetModelsById(request, taskid)
        if obj:
            id, target, password, script, mark = obj.id, obj.target, obj.password, obj.script, obj.mark

        return render(request, "knifeedit.html", {"userinfo": userinfo, "target": target, "password": password, "script": script, "id": id, "mark": mark})

    def post(self, request, **kwargs):
        if request.POST:
            userinfo = reqSession(request)
            target, password, id, mark = request.POST['target'], request.POST['password'], request.POST['id'], request.POST['mark']
            if userinfo:
                userinfo.myshellmodels_set.filter(id=id).update(target=target, password=password, mark=mark)
                return redirect('/knife/')
            return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

class FileAdd(View):

    def get(self, request, **kwargs):
        userinfo = reqSession(request)
        filepath = request.GET['filepath'] if request.GET.has_key("filepath") else None
        taskid = int(kwargs['taskid'])
        if userinfo and taskid and filepath:
            return render(request, "addfile.html", {"userinfo": userinfo, "taskid": taskid, "filepath": filepath})
        return render(request, "errorbase.html", {"errormsg": "用户权限错误,或是未指定文件路径"})

    def post(self, request, **kwargs):
        print kwargs
        taskid, filepath, filename, context = kwargs['taskid'], request.POST['filepath'], request.POST['filename'], request.POST['context']

        obj = GetModelsById(request, taskid)
        if obj:
            target, password, script = obj.target, obj.password, obj.script
            shell = Knife(target, password, script)
            path = filepath+'//'+filename
            ret = shell.Get_Write_File(path=path, context=context)
            if ret == {u'status': u'0'}: return redirect('/knife/task/show/{}/?dir={}'.format(taskid, filepath))
            else: return render(request, "errorbase.html", {"errormsg": "上传出错"})
        return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

# 展示用户shell
class TaskShow(View):

    def get(self, request, **kwargs):
        userinfo = reqSession(request)

        taskid = int(kwargs['taskid'])
        obj = GetModelsById(request, taskid)
        if obj:
            target, password, script = obj.target, obj.password, obj.script
            shell = Knife(target, password,script)

        # 判断是默认文件夹还是指定文件夹
            if request.GET: current_dir = request.GET['dir']
            else:
                current_dir = shell.Get_Absolute_Path()
                if current_dir.has_key('current_dir'): current_dir = shell.Get_Absolute_Path()['current_dir']
                else: current_dir = "Password Error or Shell is bad!"

            files = shell.Get_Path_File(current_dir)
            statics = map(lambda file:('success','danger')[file[-1] == '/'], files)
            return render(request, "show.html", {"Absmsg": shell.Get_Absolute_Path(), "current_dir": current_dir, "Showfiles": [{"filename": file[0], "static": file[1]} for file in zip(files, statics)], "taskid": taskid, "userinfo": userinfo})
        return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

# 删除shell
class TaskDel(View):

    def get(self, request, **kwargs):
        task_id = kwargs['taskid']
        obj = GetModelsById(request, int(task_id))
        if obj:
            obj.delete()
            return redirect('/knife/')
        return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

# shell的命令执行
class TaskCmd(View):

    def get(self, request, **kwargs):
        userinfo = reqSession(request)
        taskid = int(kwargs['taskid'])
        obj = GetModelsById(request, taskid)
        if obj:
            target, password, script = obj.target, obj.password, obj.script
            shell = Knife(target, password, script)

            # 判断是默认命令还是指定命令
            if request.GET:
                userinfo = reqSession(request)
                current_cmd = request.GET['cmd']
                ret = shell.Get_Cmd_Ret(current_cmd)
                ret['current_cmd'] = current_cmd
                return JsonResponse(ret)
            return render(request, "cmd.html", {"userinfo": userinfo})
        return render(request, "errorbase.html", {"errormsg": "用户权限错误"})

# 用户注册
class UserReg(View):

    def get(self, request):
        userinfo = reqSession(request)
        registers = UserModels.objects.all().count()
        return render(request, "regist.html", {"userinfo": userinfo, "registers": registers})

    def post(self, request):
        if request.POST:
            username, password = request.POST['username'], request.POST['password']
            if username and password:
                user = UserModels.objects
                if not user.filter(UserName=username):
                    UserSave = user.create(UserName=username, UserPass=password).save()
                    return redirect('/knife/login/')
                return render(request, 'errorbase.html', {"errormsg": "用户名已经被注册过, 请重试!"})
        return render(request, 'errorbase.html', {"errormsg": "错误的用户名和密码, 请重试!"})


# 用户登录
class UserLogin(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username, password = request.POST['username'], request.POST['password']

        UserLogin = UserModels.objects

        if username and password and UserLogin.filter(UserName=username):
            if UserLogin.get(UserName=username).UserPass == password:
                userid = UserLogin.get(UserName=username).id
                request.session['User_ID'] = userid
                return redirect('/knife/')
        return render(request, "errorbase.html", {"errormsg": "用户账号或者密码错误"})

# 用户退出
class UserLogout(View):

    def get(self, request):
        if reqSession(request):
            del request.session['User_ID']
        return redirect('/knife/')

# 测试页面
class TestView(View):

    def get(self, request):
        return render(request, "addfile.html")