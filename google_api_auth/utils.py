import dataclasses

from typing import Any

import google_auth_oauthlib.flow
import jwt
import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy


@dataclasses.dataclass
class GoogleSdkLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@dataclasses.dataclass
class GoogleAccessTokens:
    id_token: str
    access_token: str

    def decode_id_token(self) -> dict[str, Any]:
        id_token = self.id_token
        decoded_token = jwt.decode(
            jwt=id_token,
            options={"verify_signature": False}
        )
        return decoded_token


def google_sdk_login_validate_credentials(
    credential: str,
) -> [None | ImproperlyConfigured]:
    credentials = {
        "client_id": "GOOGLE_OAUTH2_CLIENT_ID",
        "client_secret": "GOOGLE_OAUTH2_CLIENT_SECRET",
        "project_id": "GOOGLE_OAUTH2_PROJECT_ID",
    }

    if not credential:
        raise ImproperlyConfigured(
            f"{credentials.get(credential)} missing in env."
        )


def google_sdk_login_get_credentials() -> GoogleSdkLoginCredentials:
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    google_sdk_login_validate_credentials(client_id)
    google_sdk_login_validate_credentials(client_secret)
    google_sdk_login_validate_credentials(project_id)

    credentials = GoogleSdkLoginCredentials(
        client_id=client_id,
        client_secret=client_secret,
        project_id=project_id
    )

    return credentials


def get_jwt_pair_token(email: str, password: str) -> dict:
    domain = settings.BASE_BACKEND_URL
    token_url = reverse_lazy("token_obtain_pair")
    token_redirect_url = f"{domain}{token_url}"

    return requests.post(
        token_redirect_url,
        data={
            "email": email,
            "password": password,
        }
    ).json()


class GoogleSdkLoginFlowService:
    API_URI = reverse_lazy("google_auth_api:callback-sdk")

    GOOGLE_CLIENT_TYPE = "web"
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    GOOGLE_AUTH_PROVIDER_CERT_URL = ""

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_sdk_login_get_credentials()

    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self):
        client_config = {
            self.GOOGLE_CLIENT_TYPE: {
                "client_id": self._credentials.client_id,
                "project_id": self._credentials.project_id,
                "auth_uri": self.GOOGLE_AUTH_URL,
                "token_uri": self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                "auth_provider_x509_cert_url": self.GOOGLE_AUTH_PROVIDER_CERT_URL,
                "client_secret": self._credentials.client_secret,
                "redirect_uris": [self._get_redirect_uri()],
                "javascript_origins": [],
            }
        }
        return client_config

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        google_oauth_flow = (
            google_auth_oauthlib.flow.Flow.from_client_config(
                client_config=client_config, scopes=self.SCOPES
            )
        )
        google_oauth_flow.redirect_uri = redirect_uri

        authorization_url, state = google_oauth_flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="select_account",
        )
        return authorization_url

    def get_tokens(self, *, code: str, state: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=client_config,
            scopes=self.SCOPES,
            state=state
        )
        flow.redirect_uri = redirect_uri
        access_credentials_payload = flow.fetch_token(code=code)

        if not access_credentials_payload:
            raise ValueError("Failed to obtain tokens from Google.")

        google_tokens = GoogleAccessTokens(
            id_token=access_credentials_payload["id_token"],
            access_token=access_credentials_payload["access_token"]
        )

        return google_tokens
