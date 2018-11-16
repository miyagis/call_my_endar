import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = {
    'readonly': 'https://www.googleapis.com/auth/calendar.readonly',
    'events': 'https://www.googleapis.com/auth/calendar.events',
    'all_access': 'https://www.googleapis.com/auth/calendar'
}

EVENT = {
  'summary': 'Testjen aja',
  'location': 'Rampelberg 1, 9310 Baardegem, Belgium',
  'description': 'Descriptiones.',
  'start': {
    'dateTime': '2018-12-06T09:00:00-07:00',
    'timeZone': 'Europe/Brussels',
  },
  'end': {
    'dateTime': '2018-12-08T17:00:00-07:00',
    'timeZone': 'Europe/Brussels',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=1'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

def insert_event(service, test_value):
    print("insert_event")
    EVENT["summary"] = test_value
    event_result = service.events().insert(calendarId='primary', body=EVENT).execute()

def get_upcoming_ten_events(service, maxResults):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming {} events'.format(maxResults))
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=maxResults, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def authorize(creds):
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def get_creds(scope):
    token_file = 'tokens/token_{}.json'.format(scope)
    print(token_file)
    store = file.Storage(token_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES['events'])
        creds = tools.run_flow(flow, store)
    return creds

def main(action_type):
    if action_type == 'insert_event':
        scope = 'events'
        creds = get_creds(scope)
        service = authorize(creds)
        insert_event(service)
    else:
        get_upcoming_ten_events(service, 10)


if __name__ == '__main__':
    main()
