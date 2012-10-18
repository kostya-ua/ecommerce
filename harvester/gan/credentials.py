from __future__ import absolute_import

import httplib2

from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials, AccessTokenRefreshError, Storage
from oauth2client.tools import run

from ..models.gan import GoogleCredential
from ..models.meta import DBSession

class DBCredentialStorage(Storage):
    def put(self, credentials):
        session = DBSession()
        credential = GoogleCredential()
        for field in GoogleCredential.__table__.columns:
            field_name = field.name

            if not hasattr(credentials, field_name):
                continue

            setattr(credential, field_name, getattr(credentials, field_name))

        session.add(credential)
        session.commit()

    def refresh(self, client_id, client_secret):
        FLOW = OAuth2WebServerFlow(
            client_id=client_id,
            client_secret=client_secret,
            scope='https://www.googleapis.com/auth/gan'
        )

        return run(FLOW, self)

    def get(self):
        session = DBSession()
        settings = session.query(GoogleCredential).order_by(GoogleCredential.token_expiry.desc()).first()
        oauth_credentials = OAuth2Credentials(
            access_token=settings.access_token,
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            refresh_token=settings.refresh_token,
            token_expiry=settings.token_expiry,
            token_uri=settings.token_uri,
            user_agent=None
        )

        if oauth_credentials.access_token_expired:
            # Precheck access token for ability to save new credentials
            try:
                oauth_credentials._refresh(httplib2.Http().request)
            except AccessTokenRefreshError:
                oauth_credentials.invalid = True
            else:
                settings.access_token = oauth_credentials.access_token
                settings.refresh_token = oauth_credentials.refresh_token
                settings.token_expiry = oauth_credentials.token_expiry
                session.commit()

        if oauth_credentials.invalid:
            oauth_credentials = self.refresh(settings.client_id, settings.client_secret)

        return oauth_credentials


