from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Step 1: Generate Google auth URL
def get_auth_url():
    flow = Flow.from_client_secrets_file(
        'backend/credentials.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/auth/callback'
    )
    auth_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    return auth_url, state

# Step 2: Exchange auth code for tokens
def get_user_credentials(auth_code: str):
    flow = Flow.from_client_secrets_file(
        'backend/credentials.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/auth/callback'
    )
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials
    return credentials

# Step 3: Create calendar service from credentials
def get_calendar_service(credentials: Credentials):
    return build('calendar', 'v3', credentials=credentials)

# Step 4: Check user's calendar availability
def get_availability(service, start_time, end_time):
    calendar_id = 'primary'
    body = {
        "timeMin": start_time.isoformat() + 'Z',
        "timeMax": end_time.isoformat() + 'Z',
        "items": [{"id": calendar_id}]
    }
    events_result = service.freebusy().query(body=body).execute()
    return events_result['calendars'][calendar_id]['busy']

# Step 5: Book an event
def create_event(service, start_dt, end_dt, summary="AI Booking"):
    calendar_id = 'primary'
    event = {
        'summary': summary,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'}
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()


def get_upcoming_events(service, max_results=5):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
