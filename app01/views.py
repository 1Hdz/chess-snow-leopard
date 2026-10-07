from idlelib.pyshell import UserInputTaggingDelegator

from Tools.scripts.var_access_benchmark import read_dict
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")

def user_list(request):
    return HttpResponse("用户列表")

def user_add(request):
    return HttpResponse("添加用户")
# Create your views here.
from django.shortcuts import render, redirect

def user_list(request):
    return render(request, "user_list.html")

def user_add(request):
    return render(request, "user_add.html")


def tpl(request):
    name = "韩超发方法"
    roles = ["管理员", "CEO", "保安"]
    user_info = {"name": "郭智", "salary": 100000, "role": "CTO"}

    data_list = [
        {"name": "郭智", "salary": 100000, "role": "CTO"},
        {"name": "卢慧", "salary": 100000, "role": "CTO"},
        {"name": "赵建先", "salary": 100000, "role": "CTO"},
    ]

    return render(request, 'tpl.html', context={"n1": name, "n2": roles, "n3": user_info, "n4": data_list})


def weather(req):
    # 向天气网站发请求获取数据
    # 第三方模块: requests
    import requests

    res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=30.67&longitude=104.07&current=temperature_2m")
    data_list = res.json()
    print(data_list)

    return render(req, template_name='weather.html', context={"weather_list": data_list})


def something(request):
    # request 是一个对象，封装了用户发送过来的所有请求相关数据

    # 1. 获取请求方式 GET/POST
    print(request.method)

    # 2. 在URL上传传递值 /something/?n1=123&n2=999
    print(request.GET)

    # 3. 在请求体中提交数据
    print(request.POST)

    # 4. [响应] HttpResponse("返回内容")，内容字符串内容返回给请求者。
    # return HttpResponse("返回内容")

    # 5. [响应] 读取HTML的内容 + 渲染（替换）-> 字符串，返回给用户浏览器。
    # return render(request, 'something.html', {"title": "来了"})

    # 6. [响应] 让浏览器重新定向到其他的页面
    return redirect("https://www.baidu.com")


from django.shortcuts import render, HttpResponse,redirect
def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    # 如果是POST请求，获取用户提交的数据
    # print(request.POST)
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    if username == 'root' and password == "123":
        # return HttpResponse("登录成功")
        return redirect("http://www.chinaunicom.com.cn/")

    # return HttpResponse("登录失败")
    return render(request, 'login.html', {"error_msg": "用户名或密码错误"})

from app01.models import Department,UserInfo
def orm(request):
    # #### 1.新建 ####
    #Department.objects.create(title="运营部")
    #UserInfo.objects.create(name="武沛齐", password="123", age=19)
    #UserInfo.objects.create(name="朱虎飞", password="666", age=29)
    #UserInfo.objects.create(name="吴阳军", password="666")
    #data_list =UserInfo.objects.all()
    #print(data_list)
    #for obj in data_list:
        #print(obj.id,obj.name,obj.password,obj.age)
    #return HttpResponse("成功")

    #### 4.更新数据 ####
    UserInfo.objects.all().update(password="999")
    UserInfo.objects.filter(id=2).update(age=999)
    UserInfo.objects.filter(name="朱虎飞").update(age=999)

    return HttpResponse("成功")

def info_list(request):
    datalist=UserInfo.objects.all()
    return render(request, "info_list.html",
                  {"datalist": datalist})

def info_add(request):
    if request.method == "GET":
        return render(request, template_name='info_add.html')

    # 获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")

    # 添加到数据库
    UserInfo.objects.create(name=user, password=pwd, age=age)

    # 自动跳转
    # return redirect("http://127.0.0.1:8000/info/list/")
    return redirect("/info/list/")

# /info/delete/
def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/info/list/")