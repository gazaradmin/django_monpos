from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+[
    path('',monpos,name='monpos'),
    path('monpos',monpos,name='monpos'),
    path('monrtk',monrtk,name='monrtk'),
    path('mongeoid',monpos,name='mongeoid'),
    path('monstatic', CorsDetailView, name='monstatic'),
    path('question/',add_question,name='question'),
    path('question/<int:id>',delete_question,name='delete_question'),
    path('thanks',thanks,name='thanks'),
    path('mongeocalc',mongeocalc_hand,name='mongeocalc'),
    path('loadmonitor/<str:site>&<int:jil>',loadmonitor,name='loadmonitor'),
    path('download/<str:name>', download, name='download'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register/', signup_view, name="register"),
    path('statistic/', statistic, name="statistic"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
   ]