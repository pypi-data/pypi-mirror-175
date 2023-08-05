from trumpet_client.exceptions import TrumpetUnverfiedApiKey
from trumpet_client.exceptions import TrumpetUnverfiedWorkspace


# don't use this class
class ApiVerfication:

    def __init__(self, api_key=None):
        """
        :param api_key: this is secret api key
        """
        self.api_key = api_key

        if self.api_key is None:
            raise TrumpetUnverfiedApiKey()

    def api_token(self):
        return self.api_key


# don't use this class
class WorkspaceVerfication:

    def __init__(self, workspace=None):
        """
        :param workspace: user workspace
        """
        self.workspace = workspace
        if self.workspace is None:
            raise TrumpetUnverfiedWorkspace()
