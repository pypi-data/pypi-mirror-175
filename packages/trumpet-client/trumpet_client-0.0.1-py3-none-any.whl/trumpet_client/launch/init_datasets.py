import requests
import pandas as pd
from io import StringIO
from trumpet_client.api.crud import CRUD_API
from urllib import request


class Datasets:
    def make_csv(self, data_link=None):
        return requests.get(url=data_link).content

    def search_datasets(self, workspace_id=None, auth=None):
        dataset_list = CRUD_API.datasets().read(id=workspace_id, auth=auth)['resResult']
        file_list = [dataset_file['file'].split("/")[-1] for dataset_file in dataset_list]
        print(f"datasets list registered in the workspace ID: {workspace_id}")
        for index, file_name in enumerate(file_list):
            print(str(index+1)+".", file_name)

    def get_dataset(self, dataset_name=None, workspace_id=None, auth=None):
        select_dataset = self.check_dataset(dataset_name=dataset_name, workspace_id=workspace_id, auth=auth)
        download_dataset = CRUD_API.s3().get(artifact_type="datasets", json={"filePath": select_dataset[0]}, auth=auth["Authorization"]["Authorization"])
        return StringIO(str(self.make_csv(data_link=download_dataset['resResult']), "utf-8"))

    def check_dataset(self, dataset_name=None, workspace_id=None, auth=None):
        dataset_list = CRUD_API.datasets().read(id=workspace_id, auth=auth)['resResult']
        file_list = [dataset_file['file'].split("/")[-1] for dataset_file in dataset_list]
        if dataset_name in file_list:
            return [name['file'] for name in dataset_list if dataset_name == name['file'].split("/")[-1]]
        return False

    def get_download_dataset(self, dataset_name, workspace_id, auth):
        file_url = self.check_dataset(dataset_name=dataset_name, workspace_id=workspace_id, auth=auth)[0]
        dataset_url = CRUD_API.s3().get(artifact_type="datasets", json={"filePath": file_url}, auth=auth["Authorization"]["Authorization"])
        request.urlretrieve(dataset_url["resResult"], dataset_name)
        return f"{dataset_name} download was successful."


class InitDatasets(Datasets):
    def __init__(self,
                 api_key=None,
                 user_id=None,
                 workspace_id=None,
                 project_id=None):

        self.__api_key = api_key
        self.__user_id = user_id
        self.__workspace_id = workspace_id
        self.__project_id = project_id
        self.authorization = CRUD_API.user(auth=True).auth(json={"api_key": self.__api_key})

    def load_list(self):
        self.search_datasets(self.__workspace_id, auth=self.authorization)

    def load_datasets(self, dataset_name=None):
        return self.get_dataset(dataset_name=dataset_name, workspace_id=self.__workspace_id, auth=self.authorization)

    def download_dataset(self, dataset_name=None):
        return self.get_download_dataset(dataset_name=dataset_name, workspace_id=self.__workspace_id, auth=self.authorization)
