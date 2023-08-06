"""
Authentication class definitions.
"""
import base64
import copy
from abc import ABC, abstractmethod

class AuthCredentials(ABC):
    """
    Base class for getting the grant type and credentials.
    """

    def __init__(self):
        self._credentials_body = {}

    @abstractmethod
    def get_credentials(self) -> dict:
        """
        Get credentials.
        """

class AuthClientCredentials(AuthCredentials):
    """
    Using a client secret for authentication.
    In case of grant type client credentials.
    """

    def __init__(self, client_secret: str):
        """
        Using a client secret for authentication.
        In case of grant type client credentials.

        Parameters
        ----------
        client_secret : str
            The client secret credentials, NOT access token.
        """

        super().__init__()
        self._credentials_body["grant_type"] = "client_credentials"
        self._client_secret_encoded = base64.b64encode(client_secret.encode('utf-8')).decode('utf-8')

    def get_credentials(self) -> dict:
        """
        Get decoded credentials.

        Returns
        -------
        dict
            Decoded credentials.
        """

        return_body = copy.deepcopy(self._credentials_body)
        return_body["client_secret"] = (
            base64.b64decode(self._client_secret_encoded.encode('utf-8'))
            .decode('utf-8')
        )
        return return_body


class AuthClientPassword(AuthCredentials):
    """
    Using username and password for authentication.
    In case of grant type password.
    """

    def __init__(self, username: str, password: str) -> None:
        """
        Using username and password for authentication.
        In case of grant type password.

        Parameters
        ----------
        username : str
            The username to login with.
        password : str
            Password fot the given User.
        """

        super().__init__()
        self._credentials_body["grant_type"] = "password"
        self._credentials_body["username"] = username
        self._password_encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    def get_credentials(self) -> dict:
        """
        Get decoded credentials.

        Returns
        -------
        dict
            Decoded credentials.
        """

        return_body = copy.deepcopy(self._credentials_body)
        return_body["password"] = (
            base64.b64decode(self._password_encoded.encode('utf-8'))
            .decode('utf-8')
        )
        return return_body
