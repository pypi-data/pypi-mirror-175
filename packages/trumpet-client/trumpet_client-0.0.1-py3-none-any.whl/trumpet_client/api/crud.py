from trumpet_client.api import api_var
from trumpet_client.config.api_config import (DEFAULT_PROTOCOL, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_URL)
class CRUD_API:
    def __init__(self, api_key, version=api_var.DEFAULT_VERSION):
        self.version = version
        self.api_key = api_key

    class workspace(api_var.CRUD):
        def __init__(self,check_workspace=None):

            if check_workspace == "workspace_read":
                end_point = "workspace_read"
            else:
                end_point = "workspace"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class project(api_var.CRUD):
        def __init__(self):
            end_point = "project"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class experiments(api_var.CRUD):
        def __init__(self):
            end_point = "experiments"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class datasets(api_var.CRUD):
        def __init__(self):
            end_point = "datasets"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class s3(api_var.CRUD):
        def __init__(self):
            end_point = "s3"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

        def get(self, headers={}, json={}, params={}, auth={}, artifact_type=None, data=None):
            method_name="post"
            return self.request(self.end_point, method_name, headers=headers, params=params, json=json, auth=auth, data=data, artifact_type=artifact_type)

    class model(api_var.CRUD):
        def __init__(self, check_model=None):
            if check_model == "project_model":
                end_point = "project_model"
            elif check_model == "model_detail":
                end_point = "model_detail"
            else:
                end_point = "model"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class team(api_var.CRUD):
        def __init__(self):
            end_point = "team"
            version = "v1"
            super().__init__(end_point=end_point, version=version)

    class user(api_var.CRUD):
        def __init__(self, auth=None):
            if auth:
                end_point = "auth"
                version = "v2"
            else:
                end_point = "user"
                version = "v1"
            super().__init__(end_point=end_point, version=version)

        def read(self, headers={}, json={}, params={}, data=None):
            method_name = "info"
            return self.request(self.end_point, method_name, headers, json, params, data)

        def auth(self, headers={}, json={}, params={}, data=None):
            method_name = "post"
            return self.request(self.end_point, method_name, headers, json, params, data)

    class artifact(api_var.CRUD):
        def __init__(self):
            end_point = "artifact"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class artifact_set(api_var.CRUD):
        def __init__(self):
            end_point = "artifact_set"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class metric(api_var.CRUD):
        def __init__(self):
            end_point = "metric"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    class init(api_var.CRUD):
        def __init__(self):
            end_point = "init"
            version = "v2"
            super().__init__(end_point=end_point, version=version)

    # class ProjectModel(api_var.CRUD):
    #     def __init__(self):
    #         end_point = "project_model"
    #         version = "v2"
    #         super().__init__(end_point=end_point, version=version)


## 임시 방편
## DEFAULT_URL = f"{DEFAULT_PROTOCOL}://{DEFAULT_HOST}:{DEFAULT_PORT}/api"
    # return requests.get(url=f"{DEFAULT_URL}/core/workspace/{workspace_id}").json()["resResult"]["teamId"]
import requests
def get_workspace_info(workspace_id):
    return requests.get(url=f"{DEFAULT_URL}/core/workspace/{workspace_id}").json()["resResult"]["teamId"]
    # return requests.get(url=f"http://localhost:32081/api/core/workspace/{workspace_id}").json()["resResult"]["teamId"]
