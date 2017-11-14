from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django import forms

from core.forms import SignUpForm

from django.http import HttpResponse
import MySQLdb
import base64
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import hashlib

def verifymail(request):
    context={}
    if request.method == 'POST':
        email_id=request.POST.get('email')
        if email_id:
            current_site = get_current_site(request)
            message = render_to_string('core/acc_active_email.html', { 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(email_id)),
                'token': account_activation_token.make_token(email_id),
            })
            mail_subject = 'Activate your account.'
            to_email = email_id
            email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                email.send()
                context["message"]="Email sent! Verify your email-id."
                return render(request,'core/verifymail.html',context)  
            except:
                context["message"]="Network issue"
                return render(request,'core/verifymail.html',context)
    else:
        # render form to input email id to verifymail
        return render(request,'core/verifymail.html',context)


def activate(request, uidb64,token):
    # if request.session.has_key('user_id'):
    #   rollno=request.session.get('user_id')
    #   return render(request,'blog/homee.html',{'user_id':rollno,'messagee':'Logout from current account to activate other account!!'})
    # else:


    context ={}
    uid = force_text(urlsafe_base64_decode(uidb64))
    uid=uid.encode('utf-8')
    if uid and account_activation_token.check_token(uid, token):
        context["email"]=uid
        return signup(request,uid)
    else:
        context["message"]="Activate your account"
        return render(request,'core/verifymail.html',context)


def signup(request,uid):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:

        form = SignUpForm()
        form.email=uid
        form.fields['email'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['value'] = uid
        print form.email


    return render(request, 'core/signup.html', {'form': form})

