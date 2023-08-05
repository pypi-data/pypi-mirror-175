from trumpet_client.exceptions import *
from trumpet_client.config.api_config import *
from trumpet_client.utils.api_utils import *


class CRUD:
    def __init__(self, end_point, version=DEFAULT_VERSION, headers={}, json={}, params={}):
        self.end_point = end_point
        self.version = version
        self.headers = headers
        self.json = json
        self.params = params

    def request(self, end_point, method_name, headers, json, params, data, files=None, id=None, auth=None, artifact_type=None):
        end_point = end_point.lower()
        method_name = method_name.lower()

        try:
            url = get_url(self.version)
            end_point = get_end_point(end_point, self.version)
            method = get_method(method_name, self.version)
        except Exception as e:
            message = str(e)
            print(message)
            raise TrumpetClientException(message)
        try:
            if id is not None or artifact_type is not None:
                response = browse_param_requests(url=url, end_point=end_point, id=id, json=json, auth=auth, artifact_type=artifact_type)
            else:
                # url = 'http://192.168.1.131:9081/api'
                response = get_request(url=url, end_point=end_point, json=json, headers=headers, method_name=method_name, params=params, version=self.version, data=data, files=files)
        except Exception as e:
            message = str(e)
            print(message)
            return TrumpetClientException(message)
        # results = response.json()
        # if end_point.split("/")[-2] == "login":
        #     results["Authorization"] = response.headers
        results = response.json()
        # print(response.text, "@")
        results["Authorization"] = response.headers
        return results

    def create(self, headers={}, json={}, params={}, data=None, files=None, auth=None):
        method_name = "create"
        return self.request(self.end_point, method_name, headers, json, params, data, files, auth=auth)

    def read(self, headers={}, json={}, params={}, data=None, files=None, id=None, auth=None):
        method_name = "read"
        return self.request(self.end_point, method_name, headers, json, params, data, files, id=id, auth=auth)

    def update(self, headers={}, json={}, params={}, data=None, files=None):
        method_name = "update"
        return self.request(self.end_point, method_name, headers, json, params, data, files)

    def delete(self, headers={}, json={}, params={}, data=None, files=None):
        method_name = "delete"
        return self.request(self.end_point, method_name, headers, json, params, data, files)
