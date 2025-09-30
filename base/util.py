import re
from urllib.parse import urlparse
from datetime import datetime, date
from .models import ContactInfo, User
import hashlib 
import random

CONTACT_PATTERNS = {
    "Facebook": r"(?:https?:\/\/)?(?:www\.)?facebook\.com\/[A-Za-z0-9\.]+\/?",
    "Instagram": r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/[A-Za-z0-9_\.]+\/?",
    "TikTok": r"(?:https?:\/\/)?(?:www\.)?tiktok\.com\/@?[A-Za-z0-9_.]+\/?",
    "YouTube": r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(channel\/|c\/|@|user\/)?[A-Za-z0-9_\-]+|youtu\.be\/[A-Za-z0-9_\-]+)",
    "LinkedIn": r"(?:https?:\/\/)?(?:[a-z]{2,3}\.)?linkedin\.com\/(in|company)\/[A-Za-z0-9_\-]+\/?",
    "GitHub": r"(?:https?:\/\/)?(?:www\.)?github\.com\/[A-Za-z0-9_\-]+\/?",
    "X(Twitter)": r"(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/[A-Za-z0-9_]+\/?",
    "others": re.compile(r'^\+?[0-9\s().-]{6,20}$')
}

number_based_contact = ['Phone Number', 'WhatsApp', 'Viber', 'Telegram', 'Signal', 'Imo']
link_based_contact = ["Facebook", "Instagram", "TikTok", "YouTube", "LinkedIn", "GitHub", "X(Twitter)"]
searchCriteria = {'Gender': 'gender', 'Blood Group': 'blood_group', 'Job Type': 'job_type'}

contact_error = {}


def validateContacts(post, user):
  contact_types = post.getlist("contact_type[]")
  contact_values = post.getlist("contact_value[]")
  user.contacts.all().delete()

  contacts_type_value = zip(contact_types, contact_values)
  unique_contact_type_value = {}
  for contact_type, contact_value in contacts_type_value:
    if contact_type not in unique_contact_type_value:
      unique_contact_type_value[contact_type] = contact_value
      contact_type = contact_type.strip()
      contact_value = contact_value.strip()
      if contact_type and contact_value:
        if contact_type in number_based_contact:
          saveNumberBasedContact(user, contact_type, contact_value)
        elif contact_type in link_based_contact:
          saveLinkBasedContact(user, contact_type, contact_value) 
        else:
          contact_error.update({contact_type: contact_value})

  return contact_error

def saveNumberBasedContact(user, contact_type, contact_value):
  phone_regex = CONTACT_PATTERNS["others"]
  if phone_regex.fullmatch(contact_value):
      # print(contact_type, contact_value)
      ContactInfo.objects.create(user=user, type=contact_type, value=contact_value)
  else:
    contact_error.update({contact_type: contact_value})
  
def getUserAge(date_of_birth):
  date_of_birth_string = str(date_of_birth)
  dob_format = "%Y-%m-%d"
  birth_date = datetime.strptime(date_of_birth_string, dob_format).date()
  today = date.today()
  age = today.year - birth_date.year
  if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1
  return str(age)



def saveLinkBasedContact(user, contact_type, contact_value):
  parsed = urlparse(contact_value)
  if not parsed.scheme:
    contact_value = "https://" + contact_value 
  if re.fullmatch(CONTACT_PATTERNS[contact_type], contact_value):
    # print(contact_type, contact_value)
    ContactInfo.objects.create(user=user, type=contact_type, value=contact_value)
  else:
    contact_error.update({contact_type: contact_value})



def getUserFormErrorMessage(form):
  errorMessage = ""
  for field, errors in form.errors.items():
    errorMessage += getCorrespondingFieldName(field) + ": "
    for error in errors:
      errorMessage += error.strip() + " "
  return errorMessage



def getUserCreationFormErrorMessage(form):
  errorMessage = ""
  for field, errors in form.errors.items():
    for error in errors:
      errorMessage += error.strip() + " "
  return errorMessage


def getContactErrorMessage(contact_error):
   errorMessage = ""
   for key, value in contact_error:
     errorMessage += 'Invalid platform ' + key + " or it's value" + '"' + value + '"; '

   return errorMessage   


def getCorrespondingFieldName(field):
  print(field)
  if field == "name":
    return "Full Name"
  elif field == "profile_bio":
    return "Bio"
  elif field == "date_of_birth":
    return "Date of Birth"
  elif field == "gender":
    return "Gender"
  elif field == "blood_group":
    return "Blood Group"
  else:
    return field
  

def getUserContacts(allContactInfo):
  numbers = []
  links = []
  for contactInfo in allContactInfo:
    if contactInfo.type in number_based_contact:
      numbers.append({"type": contactInfo.type, "value": contactInfo.value})
    elif contactInfo.type in link_based_contact:
      links.append({"type": contactInfo.type, "value": contactInfo.value})
  
  if not numbers or not links:
    return None

  return {"numbers": numbers, "links": links}

    

  

def getContactAndSocialMediaHTMLText(allContactInfo):
  string = ""
  for contactInfo in allContactInfo:
    contactType = contactInfo.type
    contactValue = contactInfo.value
    string +=  f"""<div> <label class="contact-label" for="contact-input-{contactType}">{contactType}</label>
           <div class="contact-input-box">
              <input type="hidden" name="contact_type[]" value="{contactType}"/> """
    if contactType in number_based_contact: 
      string += f'''<input type="text" class="number-based-contact contact-value-input" name="contact_value[]" value="{contactValue}" id="contact-input-{contactType}" placeholder="{getPlaceholderText(contactType)}"/>'''
    else:
      string += f'''
    <input type="text" data-platform="{contactType}" class="link-based-contact contact-value-input" value="{contactValue}" name="contact_value[]" id="contact-input-{contactType}" placeholder="{getPlaceholderText(contactType)}"/>'''
      
    string += createSVG() + "</div></div>"
  return string
              

def getPlaceholderText(contactType):
  number_based_app =  ['WhatsApp', 'Viber', 'Telegram', 'Signal', "Imo"]
  if contactType == "Phone Number":
    return 'Enter you Phone Number'
  elif contactType in number_based_app:
    return "Enter your " + contactType + " number"
  elif contactType == "YouTube":
    return "Enter your YouTube channel link"
  else:
    return "Enter your " + contactType + " account link"

def createSVG():
  return f""" 
<svg class="remove-contact" style="width: 1.5em; height: 1.5em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <title>remove contact</title>
    <path class="remove-contact-path" d="M810.65984 170.65984q18.3296 0 30.49472 12.16512t12.16512 30.49472q0 18.00192-12.32896 30.33088l-268.67712 268.32896 268.67712 268.32896q12.32896 12.32896 12.32896 30.33088 0 18.3296-12.16512 30.49472t-30.49472 12.16512q-18.00192 0-30.33088-12.32896l-268.32896-268.67712-268.32896 268.67712q-12.32896 12.32896-30.33088 12.32896-18.3296 0-30.49472-12.16512t-12.16512-30.49472q0-18.00192 12.32896-30.33088l268.67712-268.32896-268.67712-268.32896q-12.32896-12.32896-12.32896-30.33088 0-18.3296 12.16512-30.49472t30.49472-12.16512q18.00192 0 30.33088 12.32896l268.32896 268.67712 268.32896-268.67712q12.32896-12.32896 30.33088-12.32896z"  /></svg> 
"""
  


def getSearchedUser(post):
  searchCriteriaValue = searchCriteria[post.get("search-criteria")]
  if searchCriteriaValue:
    return {searchCriteriaValue: post.get("search-value")}
  return None

def getHomePageContextDict(users, method):
  context = {'method': method}
  if not users:
    if method == 'POST':
      context['homePage'] = "No user was found with the specified information."
    else:
      context['homePage'] = "No user exist yet, please ask everyone to join."
  else:
    context['users'] = users
  return context




def saveProfilePhotoAndResume(user, request):
  profilePhotoStatus = request.POST.get("profile-photo-status")
  resumeStatus = request.POST.get('resume-status')
  existing_user = User.objects.get(pk=user.id)
  print("saving profile photo and resume")

  if profilePhotoStatus == 'changed':
    pass
  elif profilePhotoStatus == 'initial':
    user.avatar = None
  else: 
    user.avatar = existing_user.avatar

  if resumeStatus == 'changed':
    pass
  elif resumeStatus == 'initial':
    user.resume = None
  else:
    user.resume = existing_user.resume
  
  user.save()


def getRegistrationKeys(number_of_key):
  asciiCharacters = "#$%&*+0123456789=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
  registrationKey = set()
  for i in range(number_of_key):
     registrationKey.add(''.join(random.sample(asciiCharacters, 8)))
  return list(registrationKey)



def getEncryptedValue(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()



# def extract_custom_errors(form):
#     # Your custom error extraction logic
#     return " | ".join(
#         f"{field}: {', '.join(errors)}"
#         for field, errors in form.errors.items()
#     )