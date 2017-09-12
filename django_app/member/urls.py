from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    # MyUser
    url(r'^login/$', views.LoginView.as_view(), name='login'),
url(r'^login/facebook/$', views.FaceBookLoginView.as_view(), name='facebook_login'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^profile/(?P<user_pk>[0-9]+)/$', views.MyProfileView.as_view(), name='my_profile'),
    url(r'^change/password/(?P<user_pk>[0-9]+)/$', views.ChangePasswordView.as_view(), name='change_password'),

    # Tutor
    url(r'^tutor/register/$', views.TutorRegisterView.as_view(), name='tutor_register'),
]