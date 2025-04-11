
from django.urls import path

from . import views

urlpatterns = [
    path("", views.main , name="main"),
    path("signup",views.postsignup,name="signup"),
    path("login",views.getlogin,name="getlogin"),
    path("postlogin",views.postlogin,name="postlogin"),
    path("logout",views.logout,name="logout"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("createpost",views.getpostcreation,name="postcreator"),
    path("publishpost",views.publishpost,name="publishpost"),
    path("deletepost",views.deletepost,name="deletepost"),
    path("updatepost",views.updatepost,name="updatepost"),
    path("likepost/<int:id>",views.likepost,name="likepost"),
    path("dislikepost/<int:id>",views.dislikepost,name="dislikepost"),
    path("fullpost/<int:id>",views.fullpost,name="fullpost"),
    path("test",views.test,name="test"),
    path("test/",views.test,name="test")
]   

#path("postview",views.miniposts,name="miniposts"),
#if miniposts needed elsewhere othre then main page maybe not rigght now