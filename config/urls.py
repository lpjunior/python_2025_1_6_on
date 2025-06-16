from django.contrib import admin
from django.urls import path
from app.views import ServerInfoView, HelloWorldView, WelcomeView, PeopleView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('server-info/', ServerInfoView.as_view(), name='server_info'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('people/', PeopleView.as_view(), name='people'),
]