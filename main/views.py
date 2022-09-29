from django.shortcuts import render
from django.http import HttpResponse
from uuid import uuid4
from nordigen import NordigenClient

# Create your views here.
def index(request):
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id="SECRET_ID",
        secret_key="SECRET_KEY"
    )

    # Create new access and refresh token
    # Parameters can be loaded from .env or passed as a string
    # Note: access_token is automatically injected to other requests after you successfully obtain it
    token_data = client.generate_token()

    # Use existing token
    client.token = "YOUR_TOKEN"

    # Exchange refresh token for new access token
    new_token = client.exchange_token(token_data["refresh"])

    # Get institution id by bank name and country
    institution_id = client.institution.get_institution_id_by_name(
        country="LV",
        institution="Revolut"
    )

    # Get all institution by providing country code in ISO 3166 format
    institutions = client.institution.get_institutions("LV")

    # Initialize bank session
    init = client.initialize_session(
        # institution id
        institution_id=institution_id,
        # redirect url after successful authentication
        redirect_uri="https://nordigen.com",
        # additional layer of unique ID defined by you
        reference_id=str(uuid4())
    )

    # Get requisition_id and link to initiate authorization process with a bank
    link = init.link # bank authorization link
    requisition_id = init.requisition_id
    return HttpResponse("Hello, world. You're at the polls index.")