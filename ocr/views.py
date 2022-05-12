import base64
from urllib import request
from django.conf import settings

import numpy as np
import pytesseract
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
import cv2 as cv
from PIL import Image
from .forms import LoginForm, RegistrationForm

from .models import User
import bcrypt

# you have to install tesseract module too from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)

def basepage(request, username=None):
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        return render(request,"base.html",{"user":user})
        
def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))

        img = np.array(Image.open(image))
        # cv_img = cv.imread(image)
        # cv.imshow(cv_img)
        gr_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        norm_img = cv.normalize(gr_img, None, 0, 300, cv.NORM_MINMAX)
        thinned = cv.ximgproc.thinning(gr_img)
        ret, thresh_img = cv.threshold(norm_img, 120, 255, cv.THRESH_TOZERO)
        text = pytesseract.image_to_string(norm_img, lang=lang)
        # return text to html
        path =  "/static/"
        print(path)
        f = open("./static/demo.txt", "w+")
        f.write(text)
        f.close()
        return render(request, "home.html", {"ocr": text, "image": image_base64, "url": "demo.txt"}) 


    return render(request, "home.html")

def dashboardpage(request):
    return render(request, "dashboard.html")

def loginpage(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "login.html", {"form": form, "msg" : msg})


def registerpage(request):
    msg     = None
    success = False

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            return redirect("login")

        else:
            msg = 'Form is not valid'    
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form, "msg" : msg, "success" : success })

def profile(request, username=None):
    if User.objects.get(username=username):
        user = User.objects.all()
        return render(request,"dashboard.html",{"user" : user,})


def logoutUser(request):
    auth.logout(request)
    return redirect('login')


