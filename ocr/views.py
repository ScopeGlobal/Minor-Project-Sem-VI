import base64

import numpy as np
import pytesseract
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from PIL import Image
from .forms import LoginForm, RegistrationForm

from .models import User
import bcrypt

# you have to install tesseract module too from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)


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
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64})

    return render(request, "home.html")


def login(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "login.html", {"form": form, "msg" : msg})



def register(request):
    msg     = None
    success = False

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(firstname=firstname, lastname=lastname,password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            return redirect("login")

        else:
            msg = 'Form is not valid'    
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form, "msg" : msg, "success" : success })
