from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Organization
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print (request.POST)
    errorsFromModelsValidator = User.objects.registration_validator(request.POST)
    if len(errorsFromModelsValidator) > 0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        print(request.POST['password'])
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash1)
        user = User.objects.create(firstname = request.POST['fname'], lastname = request.POST['lname'], email =request.POST['email'], password = hash1.decode() )

        request.session['id'] = user.id

    return redirect("/groups")

def login(request):
    errorsFromLoginValidator = User.objects.login_validator(request.POST)
    if len(errorsFromLoginValidator)>0:
        for key, value in errorsFromLoginValidator.items():
            messages.error(request, value)
        return redirect("/")

    user = User.objects.filter(email = request.POST['email'])[0]
    print (user.id)
    request.session['id'] = User.objects.filter(email = request.POST['email'])[0].id
    return redirect("/groups")

def logout(request):
    request.session.clear()
    return redirect("/")

def home(request):

    return redirect("/groups")

def showAllGroups(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['id'])
        context = {
            "loggedinuser" : User.objects.get(id = request.session['id']),
            "allgroups": Organization.objects.all()
        }
        return render(request, "groups.html", context)

def createNewGroup(request):
    errorsFromModelsValidator = Organization.objects.org_validator(request.POST)
    loggedinuser = User.objects.get(id = request.session['id'])
    if len(errorsFromModelsValidator) > 0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect("/groups")
    org = Organization.objects.create (organization = request.POST['orgname'], description = request.POST['desc'], creator = loggedinuser)
    loggedinuser.org_joined.add(org)
    return redirect("/groups")

def GoToDetails(request, org_id):
    org = Organization.objects.get(id = org_id)
    context = {
        "org": org,
        "loggedinuser" : User.objects.get(id = request.session['id'])

    }
    return render(request, "details.html",context)

def showDetails(request, org_id):
    org = Organization.objects.get(id = org_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    context = {
        "org": org,
    }
    return render(request, "details.html", context)

def joinGroup(request,org_id):
    org = Organization.objects.get(id = org_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    loggedinuser.org_joined.add(org)
    return redirect("/groups")

def leaveGroup(request,org_id):
    org = Organization.objects.get(id = org_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    loggedinuser.org_joined.remove(org)

    return redirect("/groups")

def removeGroup(request,org_id):
    org = Organization.objects.get(id = org_id)
    org.delete()

    return redirect("/groups")


