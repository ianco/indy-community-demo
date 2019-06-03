from django.db import models

from indy_community.models import *


##############################################################
# Lab 4 - Step 3 add custom models here:
# credentials issued by an org (for the org to track against a connection)
class IssuedCredential(models.Model):
    partner = models.ForeignKey(AgentConnection, on_delete=models.CASCADE)
    credential_type = models.ForeignKey(IndySchema, on_delete=models.CASCADE)
    reference = models.ForeignKey(AgentConversation, on_delete=models.CASCADE)
    # TODO customize the data model to store individual attributes rather than a json blob
    credential_data = models.TextField(max_length=4000)

    def __str__(self):
        return self.partner + ':' + self.credential_type

# proofs received by an org (for the org to record against a connection)
class ReceivedProof(models.Model):
    partner = models.ForeignKey(AgentConnection, on_delete=models.CASCADE)
    proof_type = models.ForeignKey(IndyProofRequest, on_delete=models.CASCADE)
    reference = models.ForeignKey(AgentConversation, on_delete=models.CASCADE)
    proof_data = models.TextField(max_length=4000, blank=True)
    # TODO customize the data model to store individual attributes rather than a json blob
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.partner
##############################################################

