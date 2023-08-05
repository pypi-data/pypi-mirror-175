import io
import os
import h5py
import requests
import warnings
from operator import itemgetter
from urllib import request
from trumpet_client.config.model_config import *
from trumpet_client.exceptions import (TrumpetInfoToSameNameModel,
                                       TrumpetModelSaveFormatException,
                                       TrumpetInfoToModelVersion,
                                       TrumpetModelDownloadException,
                                       TrumpetModelNotFoundException,
                                       TrumpetModelException,
                                       TrumpetWorkspaceInNothingModel
                                       )
from trumpet_client.api.crud import CRUD_API
from trumpet_client.config.api_config import DEFAULT_URL

#TODO 추후에 requests api 분리해야함
class InquireModel:
    def search_model(self, model_id, auth):
        res = requests.get(url=f"{DEFAULT_URL}/core/model/{model_id}",
                           headers={"Authorization": auth['Authorization']['Authorization']})
        return res.json()["resResult"]["modelName"]

    def search_model_list(self, prt_id, auth):
        res = requests.get(url=f"{DEFAULT_URL}/core/project/{prt_id}/model",
                           headers={"Authorization": auth['Authorization']['Authorization']})
        return res.json()["resResult"]

    def get_workspace_list(self, workspace_id, auth):
        return CRUD_API.workspace(check_workspace="workspace_read").read(id=workspace_id, auth=auth["Authorization"]['Authorization'])

    def workspace_model_list(self, workspace_id,  auth):
        workspace_list = self.get_workspace_list(workspace_id, auth)
        prt_lists = [prt_list["prtId"] for prt_list in workspace_list["resResult"]]
        model_info_lists = sum([self.search_model_list(prt_id, auth) for prt_id in prt_lists], [])
        workspace_in_model_list = [self.search_model(model_info["modelId"], auth) for model_info in model_info_lists if (type(model_info) != int)==True]
        if workspace_in_model_list:
            contents = f"This is a list of models registered in the workspace ID: {workspace_id}.\n"
            for index, model_name in enumerate(workspace_in_model_list):
                contents += f"{index+1}. " + model_name + "\n"
            return contents
        else:
            contents = f"Currently there is no registered model in that workspaceID: {workspace_id}."
            return contents

    def get_model(self, workspace_id, auth, model_name, version=None, mode=None):
        workspace_list = self.get_workspace_list(workspace_id, auth)
        prt_lists = [prt_list["prtId"] for prt_list in workspace_list["resResult"]]
        model_info_lists = sum([self.search_model_list(prt_id, auth) for prt_id in prt_lists], [])
        user_search_model = sorted([model_infos for model_infos in model_info_lists if type(model_infos) != int],
                                   key=itemgetter("createTime"))
        user_search_model = [get_model for get_model in user_search_model if get_model["modelName"] == model_name]
        if len(user_search_model) == 0:
            raise TrumpetModelNotFoundException()
        try:
            if len(user_search_model) == 1:
                return self.file_path_to_read(user_search_model[0]["file"], auth=auth, mode=mode)
            if (len(user_search_model) > 1) and version is not None:
                 select_model_info=[model_info for model_info in user_search_model if model_info["version"] == version]
                 return self.file_path_to_read(select_model_info[0]["file"], auth=auth, mode=mode)

            if len(user_search_model) >= 2 and version is None:
                return {"workspace_id": workspace_id, "modelName": user_search_model[0]['modelName'], "model_len": len(user_search_model)}
        except:
            raise TrumpetInfoToSameNameModel(workspace_id=workspace_id, model_name=model_name, model_len=len(user_search_model))
        return None

    def download_model_list(self, model_path=None, auth=None):
       pass

    def file_path_to_read(self, model_path, auth, mode):
        res = requests.post(url=f"{DEFAULT_URL}/core/s3/download", json={"reqDetail": {"filePath": model_path}})
        file_format = res.json()["resResult"].split("model/")[1].split("?")[0].split(".")[1]
        if mode is None:
            if (file_format == "pth") or (file_format == "pt"):
                readModel = requests.get(url=res.json()["resResult"])
                return io.BytesIO(readModel.content)
            elif file_format == "h5":
                return h5py.File(io.BytesIO(requests.get(res.json()["resResult"]).content), mode="r")
        else:
            return res.json()['resResult']

    def file_download(self, workspace_id, auth, model_name, version):
        get_model_file_url = self.get_model(workspace_id=workspace_id, auth=auth, model_name=model_name, version=version, mode="download")
        if isinstance(get_model_file_url, dict):
            return TrumpetInfoToSameNameModel(workspace_id=get_model_file_url["workspace_id"], model_name=get_model_file_url["modelName"], model_len=get_model_file_url["model_len"])
        if get_model_file_url is None:
            raise TrumpetModelDownloadException(name=model_name)

        request.urlretrieve(get_model_file_url, get_model_file_url.split("model/")[1].split("?")[0])
        return "Download is complete"

    def check_model_file(self, model_file):
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

    def check_project_in_model(self, model_name=None, model_version=None, prt_id=None, workspace_id=None, auth=None):
        res = requests.get(url=f"{DEFAULT_URL}/core/project/{prt_id}/model",
                           headers={"Authorization": auth["Authorization"]['Authorization']})
        model_checker = [model for model in res.json()['resResult'] if
                         (model['modelName'] == model_name and model['version'] == model_version)]
        if len(model_checker) > 0:
            return model_checker
        else:
            return ""

    def check_model_version(self, model_name=None, model_version=None, prt_id=None, workspace_id=None, auth=None):
        model_check = self.check_project_in_model(model_name=model_name,
                                                  model_version=model_version,
                                                  prt_id=prt_id,
                                                  workspace_id=workspace_id,
                                                  auth=auth)

        if len(model_check) == 0:
            with warnings.catch_warnings():
                warnings.simplefilter("always")
                if model_version == DEFAULT_MODEL_VERSION:
                    TrumpetInfoToModelVersion(model_name)

    #TODO 실험 생성되지 않고 모델 등록할 수 있는 api 필요
    # def requests_register_model(self):
    #     pass


class InitModel(InquireModel):
    def __init__(self,
                 api_key,
                 user_id,
                 workspace_id,
                 project_id
                 ):
        self.__api_key = api_key
        self.__workspace_id = workspace_id
        self.authorization = CRUD_API.user(auth=True).auth(json={"api_key": self.__api_key})

    def read_model(self, model_name, version=None):
        return self.get_model(self.__workspace_id, self.authorization, model_name=model_name, version=version)

    def read_model_list(self):
        print(self.workspace_model_list(workspace_id=self.__workspace_id, auth=self.authorization))

    def download_model(self, model_name, version=None):
        print(self.file_download(model_name=model_name, version=version, workspace_id=self.__workspace_id, auth=self.authorization))
