from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import User, Registration
from .forms import MyUserCreationForm, UserInfoForm, EmailForm
from django.contrib.auth.forms import PasswordChangeForm
import random
from django.core.mail import send_mail
from datetime import  timedelta
from django.utils import timezone
from django.db.models import Q
from .util import validateContacts, getContactErrorMessage, getUserFormErrorMessage, getUserCreationFormErrorMessage, getUserAge, getUserContacts, getContactAndSocialMediaHTMLText, getSearchedUser, getHomePageContextDict, saveProfilePhotoAndResume, getEncryptedValue, getRegistrationKeys
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@login_required(login_url='login')
def homePage(request):
  users = None
  method = ''
  if request.method == "POST":
    filter_kwargs = getSearchedUser(request.POST)
    if filter_kwargs:
      users = User.objects.filter(
        ~Q(profile_bio=None) &
        ~Q(id=request.user.id) &
        Q(**filter_kwargs)
      )
      method = 'POST'
  else:
    users = User.objects.filter(
      ~Q(profile_bio=None) &
      ~Q(id=request.user.id)
    )
    method = 'GET'
  context = getHomePageContextDict(users, method)
  return render(request, "base/home.html", context) 

@login_required(login_url='login')
def userPage(request, pk):
  user = User.objects.get(id=pk)
  age = getUserAge(user.date_of_birth)
  contacts = getUserContacts(user.contacts.all())
  context = {'user': user, "age": age, "contacts": contacts}
  return render(request, "base/user.html", context) 

# request.POST = {
#     'first_name': 'Kaushiq',
#     'age': '25',
#     'csrfmiddlewaretoken': 'XYZ123...'
# }
# This is the format of request object; as long as the name attribute matches the original model field name you can use any html element (i.e input, textarea, select whatever you want). If you use same name attribute for different element the last element name will be found using request.POST.get("name_attribut") but using getList() method you can get all the element value. This is what I did for contact_type[] and contact_value[] elements;
@login_required(login_url='login')
def userFormPage(request):
  context = {"header": "One More Step", "body": "Please complete your profile to continue."}
  if request.method == "POST":
    form = UserInfoForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      print("form valid")
      user = form.save(commit=False)
      saveProfilePhotoAndResume(user, request)
      contact_error = validateContacts(request.POST, user)
      if contact_error:
        context['body'] = getContactErrorMessage(form)
      else:
        return redirect('userPage', pk=user.id)
    else:
      context['body'] = getUserFormErrorMessage(form)
    context['header'] = 'Error'
  
  if request.user.has_complete_profile():
     user = request.user
     contactAndSocialMediaHTMLText = getContactAndSocialMediaHTMLText(user.contacts.all())
     context["user"] = user
     context['contactAndSocialMediaHTMLText'] = contactAndSocialMediaHTMLText
  else:
     context['user'] = "user"
     context['userFormPage'] = "userFormPage"
  return render(request, "base/user_form.html", context) 

def check_if_superuser(user):
    return user.is_superuser

@login_required(login_url='login')
@user_passes_test(check_if_superuser)
def getRegKeyPage(request):
  if request.method == "POST":
    value = int(request.POST.get("input-value"))
    registrationKeys = getRegistrationKeys(value)
    for registrationKey in registrationKeys:
      Registration.objects.create(
        registrationKey = registrationKey
      )
    return redirect("getRegKeyPage")
     
  registrationObjs = Registration.objects.filter(is_used=False) 
  context = {"registrationObjs": registrationObjs}
  return render(request, "base/get_reg_key.html", context) 

# need to modify these views

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homePage')
    context = {'page': 'login'}
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
              login(request, user)
              return redirect('homePage')
        except:
            pass
        context['loginError'] = 'Invalid email or password.'
        context['email'] = email
        context['password'] = password
    else: 
       context['success'] = request.session.pop("register-success", None)
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def changePassword(request):
   context = {'oldPassword': 'oldPassword'}
   if request.method == 'POST':
      form = PasswordChangeForm(request.user, request.POST)
      if form.is_valid():
          user = form.save()
          update_session_auth_hash(request, user)  # Important!
          messages.success(request, 'Your password was successfully updated!')
          return redirect('homePage')
      else:
          context["passwordResetError"] = getUserCreationFormErrorMessage(form)
   return render(request, 'base/reset_password_form.html', context)

def sendOTP(request):
  context = {'page': 'page'} # for not showing the navbar
  email = None
  registrationKey = None
  if request.method == 'POST':
    form = EmailForm(request.POST)
    if form.is_valid(): 
      email = form.cleaned_data['email']
      registrationKey = form.cleaned_data['registrationKey']
      try:
         user = User.objects.get(email=email)
         deleteRegKeyObj(registrationKey)
      except:
         try:
            registrationObj = Registration.objects.get(registrationKey=registrationKey)
            sendMail(registrationObj=registrationObj, email=email)
            request.session['regKeyObjId'] = registrationObj.id
            return redirect("verifyOTP")
         except:
            pass
    context['formError'] = "Invalid email or registration key."
  else:
     context['formError'] = request.session.pop('session_expired', None)
  context['email'] = email
  context['registrationKey'] = registrationKey
  return render(request, 'base/send_otp.html', context)

def verifyOTP(request):
  context = {'page': 'page'} # for not showing the navbar
  regKeyObjId = request.session.get('regKeyObjId')
  try:
     registrationObj = Registration.objects.get(id=regKeyObjId)
     timeLeft = get_remaining_seconds(registrationObj.created_at)
     if request.method == 'POST':
        if timeLeft == 0:
           sendMail(registrationObj=registrationObj, email=None)
           return redirect("verifyOTP")
        else:
          if registrationObj.otp == request.POST.get("otp"):
              registrationObj.save()
              return redirect('register')
          context['otp_error'] = "Invalid otp, try again."
     context['timeLeft'] = timeLeft
     return render(request, 'base/verify_otp.html', context)
  except:
     request.session['session_expired'] = "Your session has been expired, please try again."
     return redirect('sendOTP')

def registerPage(request):
  context = {'page': 'register'} # for not showing the navbar
  regKeyObjId = request.session.get('regKeyObjId')
  try:
      registrationObj = Registration.objects.get(id=regKeyObjId)
      if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = registrationObj.email
            user.save()
            registrationObj.delete()
            request.session.pop('regKeyObjId', None)
            request.session['register-success'] = "Your account has been created successfully, you can now login."
            return redirect('login')
        else:
           context['registrationError'] = getUserCreationFormErrorMessage(form)
      context['email'] = registrationObj.email
      print(request.method)
      return render(request, 'base/login_register.html', context)
  except:
      request.session['session_expired'] = "Your session has been expired, please try again."
      return redirect('sendOTP')

def get_remaining_seconds(start_time):
    end_time = start_time + timedelta(seconds=120)
    now = timezone.now()
    remaining = (end_time - now).total_seconds()
    return max(0, int(remaining))

def sendMail(registrationObj, email):
    if email:
       registrationObj.email = email
    else:
       email = registrationObj.email
    otp = str(random.randint(100000, 999999))
    registrationObj.otp = otp
    send_mail(
      'Verify your email',
      f'Your verification code is: {otp}',
      'no-reply@yourdomain.com',
      [email],
      fail_silently=False,
    )
    registrationObj.is_used = True
    registrationObj.save()


def deleteRegKeyObj(registrationKey):
    try:
      registrationObj = Registration.objects.get(registrationKey=registrationKey)
      registrationObj.delete()
    except:
      pass

class MyPasswordResetView(PasswordResetView):
    template_name = 'base/reset_password/send_link.html'
    subject_template_name = 'base/reset_password/email_subject.txt'
    email_template_name = 'base/reset_password/email_body.txt'
    html_email_template_name = 'base/reset_password/email_design.html'

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()
        body_text = render_to_string(email_template_name, context)
        body_html = render_to_string(self.html_email_template_name, context)

        msg = EmailMultiAlternatives(subject, body_text, from_email, [to_email])
        msg.attach_alternative(body_html, "text/html")
        msg.send()


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["passwordResetError"] = getUserCreationFormErrorMessage(form)
        return self.render_to_response(context)