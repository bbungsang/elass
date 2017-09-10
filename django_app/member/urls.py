from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    # MyUser
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # Tutor
    url(r'^tutor/register/$', views.TutorRegisterView.as_view(), name='tutor_register'),
]