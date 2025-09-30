from django.shortcuts import redirect
from django.urls import reverse

class baseAppMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    user = request.user
    if user.is_authenticated and not user.has_complete_profile():
        allowed_paths = [
          reverse("userFormPage"), 
          reverse("logout")
        ]
        if request.path not in allowed_paths:
          return redirect("userFormPage")
             
    return self.get_response(request)