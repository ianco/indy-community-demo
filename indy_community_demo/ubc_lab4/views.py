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
    if 'ACTIVE_ORG' in request.session:
        org_id = request.session['ACTIVE_ORG']
        org = indy_models.IndyOrganization.objects.filter(id=org_id).get()

        # TODO can do role-specific logic like:
        # if org.role.name == 'School':
        #    ...

        connections = indy_models.AgentConnection.objects.filter(wallet=org.wallet).all()

        return render(request, 'ubc_lab4/lab4_data.html', 
                    {'org': org, 
                     'org_role': org.role.name, 
                     'connections': connections})
    else:
        # TODO for individuals
        connections = []
        org = None
        return render(request, 'ubc_lab4/lab4_data.html', 
                    {'org': org, 
                     'org_role': "", 
                     'connections': connections})
    ##############################################################


##############################################################
# Lab 4 - Step 8 create a view to submit a credential offer for the new credential:
def issue_training_credential(request):
    if request.method == 'POST':
        # issue a credential of Indy
        form = IssueCredentialForm(request.POST)
        if not form.is_valid():
            return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            first_name = cd.get('first_name')
            last_name = cd.get('last_name')
            status = cd.get('status')
            year = cd.get('year')
            schema_attrs = {
                'first_name': first_name,
                'last_name': last_name,
                'status': status,
                'year': year,
            }

            wallet = indy_views.wallet_for_current_session(request)
            connection = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active', connection_type='Outbound', id=connection_id).get()
            cred_def = indy_models.IndyCredentialDefinition.objects.filter(wallet=wallet, creddef_name='Certification of Indy'+'-'+wallet.wallet_name).get()

            # call VCX to send the credential offer
            conversation = agent_utils.send_credential_offer(wallet, connection, "Indy Certification", schema_attrs, cred_def, "Indy Certification")

            # create our custom object
            issued_credential = IssuedCredential(
                    partner=connection,
                    credential_type=cred_def.ledger_schema,
                    reference=conversation,
                    credential_data=json.dumps(schema_attrs),
                )
            issued_credential.save()

            return render(request, 'indy/form_response.html', {'msg': 'Issued Indy credential'})
    else:
        # populate form and get info from user
        wallet = indy_views.wallet_for_current_session(request)
        connection_id = request.GET.get('connection_id', None)
        connections = indy_models.AgentConnection.objects.filter(id=connection_id, wallet=wallet).all()
        connection = connections[0]
        form = IssueCredentialForm(initial={'connection_id': connection.id})
        return render(request, 'ubc_lab4/lab4_issue_credential.html', {'form': form})
##############################################################


##############################################################
# Lab 4 - Step 11 create a view to submit a request to prove the new certification:
def request_training_proof(request):
    # request a proof of Indy
    wallet = indy_views.wallet_for_current_session(request)
    connection_id = request.GET.get('connection_id', None)
    connections = indy_models.AgentConnection.objects.filter(id=connection_id, wallet=wallet).all()
    connection = connections[0]
    
    proof_request = indy_models.IndyProofRequest.objects.filter(proof_req_name='Proof of Indy').get()
    proof_uuid = str(uuid.uuid4())
    proof_name = 'Proof of Indy'
    proof_attrs = proof_request.proof_req_attrs
    proof_predicates = proof_request.proof_req_predicates

    conversation = agent_utils.send_proof_request(wallet, connection, proof_uuid, proof_name, json.loads(proof_attrs), json.loads(proof_predicates)) 

    # create our custom object
    issued_proof_request = ReceivedProof(
            partner=connection,
            proof_type=proof_request,
            reference=conversation,
            proof_data="",
        )
    issued_proof_request.save()

    return render(request, 'indy/form_response.html', {'msg': 'Issued request for Indy proof'})
##############################################################


#####################################################
# event callbacks
#####################################################
# dispatcher
def conversation_callback(conversation, prev_type, prev_status):
    print(conversation.conversation_type, conversation.status, prev_type, prev_status)

    ##############################################################
    # Lab 4 - Step 13 create a view to submit a request to prove the new certification:
    # monitor received proofs and update our local table
    if conversation.conversation_type != prev_type or conversation.status != prev_status:
        if conversation.conversation_type == 'ProofRequest' and conversation.status == 'Accepted':
            print("Updating record")

            # update record
            proof_data = json.loads(conversation.conversation_data)
            libindy_proof = json.loads(proof_data["data"]["proof"]["libindy_proof"])

            issued_proof_request = ReceivedProof.objects.filter(reference=conversation).get()
            issued_proof_request.proof_data = json.dumps(libindy_proof["requested_proof"])
            issued_proof_request.save()
    ##############################################################


# dispatcher
def connection_callback(connection, prev_status):
    print("connection callback", prev_status, connection.status)

    # TODO check for connection events of interest

