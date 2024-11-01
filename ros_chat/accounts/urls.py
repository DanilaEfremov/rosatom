from django.urls import path
from .views import SignUpView, do_logout

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('do_logout/', do_logout, name='do_logout'),
]
