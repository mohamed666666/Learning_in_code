from django.shortcuts import render
import json
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

# Create your views here.



@require_POST
def Login(requst):
    data=json.load(requst.body)
    usern=data.get("username")
    passw=data.get("password")

    if usern is None or passw is None:
        return JsonResponse({"details":"please provide username and password "})
    
    usr=authenticate(username=usern,password=passw)
    if usr is None:
        return JsonResponse({"details":"credintials not correct"})
    
    login(user=usr)
    return JsonResponse({"Succesfully logedin "})

def Logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"you not logged in "})
    logout(request=request)


@ensure_csrf_cookie
def session(req):
    if not req.user.is_authenticated:
        return JsonResponse({"is_authenticated":False})
    return  JsonResponse({"is_authenticated":True})

def whoami(req):
    if not req.user.is_authenticated:
        return JsonResponse({"user":"not found"})
    return  JsonResponse({"user":req.user})