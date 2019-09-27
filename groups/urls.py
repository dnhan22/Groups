from django.urls import path
from groupsApp import views

urlpatterns = [
    path('', views.index),
    path("register", views.register),
    path("login", views.login),
    path("groups", views.showAllGroups),
    path("logout", views.index),
    path("home",views.home),
    path("addOrg", views.createNewGroup),
    path("details/<org_id>", views.GoToDetails),
    path("groups/details/<org_id>", views.showDetails),
    path("joinGroup/<org_id>", views.joinGroup),
    path("leaveGroup/<org_id>", views.leaveGroup),
    path("removeGroup/<org_id>", views.removeGroup),



    ]
