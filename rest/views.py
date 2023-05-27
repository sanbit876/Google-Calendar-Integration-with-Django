from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os

# Set environment variable to allow insecure transport for testing purposes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Path to the JSON file containing the OAuth 2.0 client credentials
CLIENT_SECRETS_FILE = "credentials.json"

# OAuth 2.0 access scopes required for the application
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

# Redirect URL for the OAuth 2.0 flow
REDIRECT_URL = 'http://127.0.0.1:8080/rest/v1/calendar/redirect'

# Google Calendar API service name and version
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'


@api_view(['GET'])
def GoogleCalendarInitView(request):
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    # Set the redirect URI for the OAuth 2.0 flow
    flow.redirect_uri = REDIRECT_URL

    # Generate the authorization URL and state for the OAuth 2.0 flow
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Enable offline access to refresh access token
        include_granted_scopes='true'  # Enable incremental authorization
    )

    # Store the state in the session for later verification
    request.session['state'] = state

    return Response({"authorization_url": authorization_url})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    # Retrieve the state from the session for verification
    state = request.session['state']

    # Create a flow instance with client secrets and state for the OAuth 2.0 flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )

    # Set the redirect URI for the OAuth 2.0 flow
    flow.redirect_uri = REDIRECT_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials in the session for future use
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    # Check if credentials are present in the session
    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    # Load the credentials from the session
    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

    # Build the Google API client using the Discovery Service
    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )

    # Retrieve the calendars on the user's calendar list
    calendar_list = service.calendarList().list().execute()

    # Get the user's ID (email address)
    calendar_id = calendar_list['items'][0]['id']

    # Retrieve all events associated with the user's ID (email address)
    events = service.events().list(calendarId=calendar_id).execute()

    events_list_append = []
    if not events['items']:
        print('No data found.')
        return Response({"message": "No data found or user credentials invalid."})
    else:
        for event in events['items']:
            events_list_append.append(event)
        return Response({"events": events_list_append})

    return Response({"error": "No calendar events found."})


def credentials_to_dict(credentials):
    """
    Converts OAuth 2.0 credentials to a dictionary format.
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }