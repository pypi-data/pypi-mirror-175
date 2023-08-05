import requests
from trumpet_client.api import crud as CRUD_API
from trumpet_client.artifact.artifact_handler import (separate_file_type,
                                                      process_hyperparameter,
                                                      process_datasets
                                                      )
from trumpet_client.exceptions import TrumpetDataSetSameNameException
from trumpet_client.config.api_config import DEFAULT_URL
class ExperimentManagement:

    def inquiry_experiment(self, exp_id, auth):
        # res = requests.get(url=f"{DEFAULT_URL}/core/exp/{exp_id}"
        #                    )

        # res = requests.get(url=f"{DEFAULT_URL}/core/exp/{exp_id}",
        #                    headers={"Authorization": auth["Authorization"]["Authorization"]}
        #                    )

        # res = requests.get(url=f"http://localhost:32081/api/core/exp/{exp_id}",
        #                    headers={"Authorization": auth["Authorization"]["Authorization"]}
        #                    )
        res = requests.get(url=f"{DEFAULT_URL}/core/exp/{exp_id}",
                           headers={"Authorization": auth["Authorization"]["Authorization"]}
                           )
        # print(res.json()['resResult'])
        # print(type(res.json()['resResult']['tag']), res.json()['resResult']['tag'])
        # print(exp_id, "exp_id")
        # print(auth["Authorization"]["Authorization"], "auth")

        return self.update_experiment_status(exp_id, auth=auth, exper_info=res.json())

    def update_experiment_status(self, exp_id, auth, exper_info):
        res = requests.put(url=f"{DEFAULT_URL}/core/exp/{exp_id}", json={"reqDetail": {
            "create_time": exper_info["resResult"]["createTime"],
            "create_user_id": exper_info["resResult"]["createUserId"],
            "description": exper_info["resResult"]['description'],
            "duration_time": exper_info["resResult"]['durationTime'],
            "end_time": exper_info["resResult"]['endTime'],
            "exp_id": exper_info["resResult"]['expId'],
            "exp_name": exper_info["resResult"]["expName"],
            "parent_id": exper_info["resResult"]['parentId'],
            "prt_id": exper_info["resResult"]["prtId"],
            "start_time": exper_info["resResult"]['startTime'],
            "update_time": exper_info['resResult']['updateTime'],
            "status": "C",
            "tag": exper_info["resResult"]['tag'][1:-1].split(',')
        }}, headers={"Authorization": auth["Authorization"]["Authorization"]})


        # res = requests.put(url=f"http://localhost:32081/api/core/exp/{exp_id}", json={"reqDetail": {
        #     "create_time": exper_info["resResult"]["createTime"],
        #     "create_user_id": exper_info["resResult"]["createUserId"],
        #     "description": exper_info["resResult"]['description'],
        #     "duration_time": exper_info["resResult"]['durationTime'],
        #     "end_time": exper_info["resResult"]['endTime'],
        #     "exp_id": exper_info["resResult"]['expId'],
        #     "exp_name": exper_info["resResult"]["expName"],
        #     "parent_id": exper_info["resResult"]['parentId'],
        #     "prt_id": exper_info["resResult"]["prtId"],
        #     "start_time": exper_info["resResult"]['startTime'],
        #     "update_time": exper_info['resResult']['updateTime'],
        #     "status": "C",
        #     "tag": exper_info["resResult"]['tag'][1:-1].split(',')
        # }},headers={"Authorization": auth["Authorization"]["Authorization"]})


class ArtifactManagement(ExperimentManagement):
    def __init__(self, artifact_setup, api_key, user_id, work_id, prt_id, exp_id, artifact_name=None):
        self.artifact_setup = artifact_setup
        self.artifact_name = artifact_name
        self.artifact_set_id = self.artifact_setup['artifactSetId']
        self.api_key = api_key
        self.artifact_id = None
        self.user_id = user_id,
        self.work_id = work_id,
        self.prt_id = prt_id,
        self.exp_id = exp_id
        self.experiment_api = CRUD_API.CRUD_API(api_key=self.api_key)
        self.header = {"api_key": self.api_key}

    def send_artifact(self, file_type=None, artifact_experiment=None, description=None):
        artifact_form, files = separate_file_type(
                                                  create_user_id=self.user_id,
                                                  artifact_name=self.artifact_name,
                                                  artifact_set_id=self.artifact_set_id,
                                                  file_type=file_type,
                                                  artifact_experiment=artifact_experiment,
                                                  description=description
                                                  )
        result = self.experiment_api.artifact().create(headers=self.header, data=artifact_form, files=files)
        return result

    def send_parameter(self, file_type=None, hyper_map=None):
        artifact_form, files = process_hyperparameter(
            artifact_name=self.artifact_name,
            artifact_set_id=self.artifact_set_id,
            file_type=file_type,
            hyper_map=hyper_map
        )
        result = self.experiment_api.artifact().create(headers=self.header, data=artifact_form, files=files)
        return result

    def confirm_dataset_name(self, dataset_name=None, file_path=None, auth=None):
        search_datasets = CRUD_API.CRUD_API.datasets().read(id=self.work_id[0], auth=auth)['resResult']

        if dataset_name is not None:
            return [file_name['file'] for file_name in search_datasets if dataset_name == file_name['file'].split("/")[-1].split(".")[0]]

        if dataset_name is None and file_path is not None:
            return [file_name['file'] for file_name in search_datasets if file_path.split("/")[-1].split(".")[0] == file_name['file'].split("/")[-1].split(".")[0]]

    # 같은 데이터 셋 이름 체크하고 하기
    def send_datasets(self, file_name=None, file_path=None, description=None, file_type=None, auth=None):
        registered_datasets = self.confirm_dataset_name(dataset_name=file_name, file_path=file_path, auth=auth)
        if len(registered_datasets) == 0:
            artifact_form, files = process_datasets(
                artifact_name="",
                artifact_set_id=self.artifact_set_id,
                file_type=file_type,
                file_name=file_path.split("/")[-1].split(".")[0] if file_name is None else file_name,
                file_path=file_path
            )
            self.experiment_api.artifact().create(headers=self.header, data=artifact_form, files= files)
            print(f"{file_name} is registered")
        else:
            if file_name is not None:
                raise TrumpetDataSetSameNameException(dataset_name=file_name)
            else:
                raise TrumpetDataSetSameNameException(dataset_name=file_path.split("/")[-1].split(".")[0])
