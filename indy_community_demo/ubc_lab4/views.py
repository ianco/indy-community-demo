from django.shortcuts import render

from .models import *
from .forms import *

import json
import uuid

import indy_community.models as indy_models
import indy_community.views as indy_views
import indy_community.agent_utils as agent_utils


#####################################################
# custom views
#####################################################
# Create your views here.
def profile_view(request):
    """
    Generic profile view (pluggable).
    """
    # TODO customize the profile view
    return render(request, 'ubc_lab4/lab4_profile.html')


def data_view(request):
    """
    Generic data view (pluggable).
    """
    ##############################################################
    # Lab 4 - Step 4 select the current org info and set of connections and pass to the template:
    # TODO customize the data view
    return render(request, 'ubc_lab4/lab4_data.html')
    ##############################################################


##############################################################
# Lab 4 - Step 8 create a view to submit a credential offer for the new credential:
# TODO
##############################################################


##############################################################
# Lab 4 - Step 11 create a view to submit a request to prove the new certification:
# TODO
##############################################################


#####################################################
# event callbacks
#####################################################
# dispatcher
def conversation_callback(conversation, prev_type, prev_status):
    print(conversation.conversation_type, conversation.status, prev_type, prev_status)

    ##############################################################
    # Lab 4 - Step 13 create a view to submit a request to prove the new certification:
    # TODO monitor received proofs and update our local table
    ##############################################################


# dispatcher
def connection_callback(connection, prev_status):
    print("connection callback", prev_status, connection.status)

    # TODO check for connection events of interest

