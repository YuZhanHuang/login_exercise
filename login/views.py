from django.shortcuts import render, redirect
from . import models
from . import forms
import hashlib
# Create your views here.

def hash_code(s, salt='mysite'):
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()



def index(request):
    pass
    return render(request,'login/index.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username',None)
#         password = request.POST.get('password',None)
#         messaage = 'all attribute must be filled!'
#         username and password check.......
#         if password and username:
#             try:
#                 user = models.User.objects.get(name=username)
#             except:
#                 message = 'username does not exist'
#                 return render(request, 'login/login.html',{'message': message})
#         if user.password == passsword:
#
#             return redirect('/index/')
#         else:
#             message = 'wrong password'
#             return render(request, 'login/login.html',{'message': message})
#         else:
#            return render(request, 'login/login.html')
#         print(username,password)
#         return redirect('/index/')
#     return render(request,'login/login.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.RegisterForm(request.POST)
        messaage = 'all attribute must be filled!'
        # username and password check.......
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = 'username does not exist'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'wrong password'
                return render(request, 'login/login.html', locals())
        else:
           return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request,'login/login.html',locals())


def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = 'Please check your information.'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['sex']
            sex = register_form.cleaned_data['username']
            if password1 != password2:
                message = 'two different password!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'this username is already existed.'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(name=email)
                if same_email_user:
                    message = 'this email is already registered'
                    return render(request, 'login/register.html', locals())

            new_user = models.User.objects.create()
            new_user.name = username
            new_user.password = hash_code(password2)
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(request,'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()#clean user's information
    return redirect('/index/')