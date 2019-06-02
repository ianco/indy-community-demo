from django.shortcuts import render


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
    # TODO customize the data view
    return render(request, 'ubc_lab4/lab4_data.html')


#####################################################
# event callbacks
#####################################################
# dispatcher
def conversation_callback(conversation, prev_type, prev_status):
    print(conversation.conversation_type, prev_type, prev_status)

    # TODO check for conversation events of interest


# dispatcher
def connection_callback(connection, prev_status):
    print("connection callback", prev_status, connection.status)

    # TODO check for connection events of interest

