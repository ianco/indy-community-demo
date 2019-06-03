from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from .views import *


# TODO add urls for custom pages and forms

##############################################################
# Lab 4 - Step 9, 12 configure url's for the new views:
# TODO once the views are available un-comment the following:
#urlpatterns = [
# TODO Step 9:
#    path('lab4_issue_credential/', issue_training_credential, name='lab4_issue_credential'),
# TODO Step 12:
#    path('lab4_request_proof/', request_training_proof, name='lab4_request_proof'),
#]
##############################################################
