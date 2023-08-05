import requests
import os
import warnings
from datetime import datetime
from trumpet_client.api import crud as CRUD_API
from trumpet_client.envs import *
from trumpet_client.utils.datetime_utils import *
from trumpet_client.config.model_config import *
from trumpet_client.exceptions import (TrumpetModelSaveFormatException,
                                       TrumpetSameModelException,
                                       TrumpetInfoToModelVersion
                                       )


# test check model list
# def check_project_in_model(model_name=None, model_version=None, prt_id=None, workspace_id=None, auth=None):
#     res = requests.get(url=f"http://localhost:32081/api/core/project/{prt_id}/model", headers={"Authorization": auth["Authorization"]['Authorization']})
#     model_checker = [model for model in res.json()['resResult'] if (model['modelName'] == model_name and model['version'] == model_version)]
#     # print(model_checker, "model_checker 조회")
#     if len(model_checker) > 0:
#         return model_checker
#     else:
#         return ""


# test register model class
def check_model_file(model_file):
    file_type = model_file.split(".")[-1]
    if file_type in ["pth", "pkl", "h5", "pt", "index"]:
        if file_type == "pth":
            differ_file_path = (os.path.basename(model_file), open(model_file, "rb"), "text/x-python")
        elif file_type == "pkl":
            differ_file_path = (os.path.basename(model_file), open(model_file, "rb"))
        else:
            differ_file_path = (os.path.basename(model_file), open(model_file, "rb"))
        return differ_file_path
    else:
        raise TrumpetModelSaveFormatException(format=model_file)


class DealWithModel:
    def __init__(self,
                 user_id=None,
                 workspace_id=None,
                 project_id=None,
                 exp_id=None,
                 team_id=None,
                 api_key=None,
                 exp_name=None,
                 model_name=None,
                 file_path=None,
                 model_version=None,
                 description=None,
                 model_tag=None,
                 artifact_set_id=None,
                 artifact_type_id=None,
                 auth=None,
                 parent_id=None,
                 is_registry="N",
                 ):
        """
        :param user_id: user_id
        :param workspace_id: workspace_id
        :param project_id: project_id
        :param exp_id: exp_id
        :param api_key: api_key
        :param exp_name: exp_name
        :param model_name: model_name
        :param file_path: file_path
        :param model_version: model_version
        :param description: description
        :param model_tag: model_tag
        :param artifact_set_id: artifact_set_id
        :param artifact_type_id: artifact_type_id
        """
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.exp_id = exp_id
        self.team_id = team_id
        self.api_key = api_key
        self.exp_name = exp_name
        self.model_name = model_name
        self.model_version = model_version
        self.description = description
        self.model_tag = model_tag
        self.model_path = file_path
        self.artifact_set_id = artifact_set_id
        self.artifact_type_id = artifact_type_id
        self.auth = auth
        self.parent_id = parent_id
        self.is_registry = is_registry
        self.model_api = CRUD_API.CRUD_API(api_key=api_key)
        self.header = {"x-api-key": api_key}

    #TODO 모델 오버라이드 할 수 있는 옵션 필요
    def requests_register_model(self):
        # model_check = check_project_in_model(model_name=self.model_name, model_version=self.model_version,
        #                                      prt_id=self.project_id,
        #                                      workspace_id=self.workspace_id, auth=self.auth)

        # with warnings.catch_warnings():
        #     warnings.simplefilter("once")
        #     TrumpetInfoToModelVersion(self.model_name)
        # if self.model_version == DEFAULT_MODEL_VERSION:
        multipart_data = {
                "acTeamId" : self.team_id,
                "accessType": "MODEL",
                "actionType":"생성",
                "updateUserId": self.user_id,
                "workId": self.workspace_id,
                "prtId": self.project_id,
                "expId": self.exp_id,
                "expName": self.exp_name,
                "modelName": self.model_name,
                "version": self.model_version,
                "createTime": datetime_formatting(now()),
                "description": self.description,
                "tag": self.model_tag,
                "artifactSetId": self.artifact_set_id,
                "artifactTypeId": self.artifact_type_id,
                "parentId": self.parent_id,
                "isRegistry": self.is_registry,
            }
        files = [
            ("file", check_model_file(self.model_path))
        ]
        ## response 결과말고 completely model save
        self.model_api.model().create(headers=self.header, data=multipart_data, files=files)
        print(f"{self.model_name} is registered model")
    # else:
    #     raise TrumpetSameModelException(model_name=self.model_name, model_version=self.model_version,
    #                                     project_id=self.project_id)
