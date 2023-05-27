Overview:

The goal of this project is to implement Google Calendar integration using Django REST API, utilizing the OAuth2 mechanism for user authentication and authorization. The project involves creating API endpoints and corresponding views to handle the OAuth flow and retrieve events from a user's calendar.

API Endpoints and Views:

/rest/v1/calendar/init/ -> GoogleCalendarInitView()

-> This view initiates step 1 of the OAuth flow, prompting the user to enter their credentials.
-> It should display a login page or redirect the user to the Google authentication page.

/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()

This view handles the redirect request sent by Google after the user has authenticated and authorized the application.
Two main tasks need to be performed within this view:
-> Retrieve the access token from the provided authorization code.
-> Get a list of events from the user's calendar using the obtained access token.

Project Steps:

1.) Set up a Django project and create the necessary Django app for calendar integration.

2.) Implement the GoogleCalendarInitView class-based view for the /rest/v1/calendar/init/ endpoint.

-> This view should render a login page or redirect the user to the Google authentication page.
-> Use the Google OAuth client library to initiate the OAuth flow and obtain the authorization code.
-> Save the authorization code securely to be used in the next step.

3.) Implement the GoogleCalendarRedirectView class-based view for the /rest/v1/calendar/redirect/ endpoint.

-> Handle the redirect request from Google containing the authorization code.
-> Use the authorization code to request an access token from Google using the OAuth client library.
-> Save the access token securely for future API requests.

4.) Fetch events from the user's Google Calendar using the obtained access token.

-> Use the Google Calendar API client library to retrieve a list of events from the user's calendar.
-> Parse the response to extract relevant event details, such as event title, start/end time, description, etc.
-> Return the list of events as a JSON response from the API.

5.) Implement any additional functionalities required, such as CRUD operations for events, creating new events, updating existing events, and deleting events.

6.) Test the implemented API endpoints and views to ensure proper integration with Google Calendar and correct retrieval of events.

Note: It's important to handle authentication and authorization securely, using proper mechanisms for storing and managing tokens, and following best practices for OAuth implementation.
