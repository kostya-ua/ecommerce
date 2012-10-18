import httplib2

from apiclient.discovery import build

from credentials import DBCredentialStorage

def some():
    storage = DBCredentialStorage()
    credentials = storage.get()

    http = httplib2.Http()
    http = credentials.authorize(http)

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console
    # to get a developerKey for your own application.
    service = build(serviceName='gan', version='v1beta1', http=http,
        developerKey='YOUR_API_KEY')

    advertisers = service.advertisers()
    params = {'role':'publishers', 'roleId':'PUBLISHER_ID'}

    # Retrieve the relevant relationships.
    list = advertisers.list(**params).execute()

    for advertiser in list['items']:
        print advertiser['name'] + ", " + advertiser['id']