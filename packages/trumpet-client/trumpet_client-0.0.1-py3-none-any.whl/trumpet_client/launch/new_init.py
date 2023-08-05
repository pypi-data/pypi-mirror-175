


import atexit
import random
from datetime import datetime
import os
from trumpet_client.api.crud import CRUD_API
from trumpet_client.backend.register_model import DealWithModel
from trumpet_client.exceptions import TrumpetInfoToUserStartStop, TrumpetClientException
from trumpet_client.launch.handler import _user_jupyter_environment
from trumpet_client.loggers.logger import *
from trumpet_client.loggers.tracking_logging import TrackingMetrics
from trumpet_client.management.api_exceptions import _is_valid_user_api
from trumpet_client.artifact.artifact_handler import artifact_setup
from trumpet_client.artifact.artifact_management import ArtifactManagement
from trumpet_client.loggers.user_env_logging import experiment_init_info
from trumpet_client.config.artifact_config import *
from trumpet_client.utils.datetime_utils import *
from trumpet_client.config.model_config import *
from trumpet_client.backend.register_datasets import DealWithDatasets
from typing import Union
from trumpet_client.config.type_config import metrics_type_check
from trumpet_client.loggers.tracking_logging import TrackingManagement
from trumpet_client.api.crud import get_workspace_info

class Init(object):
    """
    :param workspace_id: team workspace or individual workspace(private variable)
    :param project_id: project(private variable)
    :param api_key: api key(private variable)
    :param exp_name: exp_name
    :param artifact_name: artifact_name
    """
    # __slot__ = ["api_key",
    #             "user_id",
    #             "project_id",
    #             "workspace_id",
    #             "exp_name",
    #             "artifact_name",
    #             "artifact_description_dict",
    #             "tags",
    #             "description"
    #             ]

    def __init__(self,
                 api_key,
                 user_id,
                 project_id=None,
                 workspace_id=None,
                 exp_name=None,
                 artifact_name=None,
                 artifact_description_dict={},
                 tags=None,
                 description=None,
                 is_registry="N",
                 parent_id=None,
                 exp_tag=None
                 ):
        self.api_key = api_key
        self.api = CRUD_API(api_key=self.api_key)
        self.params = {}
        self.__alive = True
        if not workspace_id and project_id:
            params = {"id": project_id}
            project = self.api.project().read(params)
            if project:
                workspace_id = project["resResult"]["workId"]
        json = {
            "api_key": self.api_key
        }
        self.headers = trumpetHeader
        self.user_id = user_id
        self.__api_keyInfo = _is_valid_user_api(api_key=api_key, user_id=user_id, workspace_id=workspace_id,
                                                project_id=project_id, exp_name=exp_name, tags=tags, description=description)
        self.__user_workspace_id = workspace_id
        self.__user_team_id = get_workspace_info(workspace_id)
        self.__user_project_id = self.__api_keyInfo["resResult"]["project_id"]
        self.__user_user_id = self.__api_keyInfo["resResult"]["user_id"]
        self.__user_exp_id = self.__api_keyInfo["resResult"]["exp_id"]
        self.__user_exp_name = self.__api_keyInfo["resResult"]["exp_name"]
        self.__user_artifact_name = artifact_name
        self.artifact_set_type = SET_TYPE
        self.artifact_setup = artifact_setup(api_key=api_key,
                                             workspace_id=self.__user_workspace_id,
                                             project_id=self.__user_project_id,
                                             exp_id=self.__user_exp_id
                                             )

        self.artifact_set_id = self.artifact_setup['artifactSetId']
        # self.track_metric = TrackingMetrics(api_key=api_key, artifact_setup=self.artifact_setup)
        self.tracking_management = TrackingManagement(api_key=api_key, artifact_setup=self.artifact_setup)

        self.artifact_management = ArtifactManagement(artifact_setup=self.artifact_setup, api_key=api_key,
                                                      work_id=self.__user_workspace_id,
                                                      prt_id=self.__user_project_id,
                                                      exp_id=self.__user_exp_id,
                                                      user_id=self.__user_user_id,
                                                      artifact_name=self.__user_artifact_name,
                                                      )
        self.artifact_description_dict = artifact_description_dict

        self.start_time = now()
        if _user_jupyter_environment():
            self.artifact_management.send_artifact(file_type=SET_TYPE["conda_environment"])
            TrumpetInfoToUserStartStop(workspace_id, project_id, api_key)
        else:
            pass
            atexit.register(self.handler_exit_time)
        self.send_experiment_info_artifact()

    def send_experiment_info_artifact(self):
        if _user_jupyter_environment():
            default_file_types = [SET_TYPE["requirements"], SET_TYPE["user_os_info"]]
        else:
            default_file_types = [SET_TYPE["source_code"], SET_TYPE["requirements"], SET_TYPE["user_os_info"]]
        default_artifact_kwargs = {file_type:{"file_type": file_type} for file_type in default_file_types}
        for file_type, description in self.artifact_description_dict.items():
            if file_type in default_file_types:
                default_artifact_kwargs[file_type]["description"] = description
        for file_type, kwargs in default_artifact_kwargs.items():
            self.artifact_management.send_artifact(**kwargs)

    def alive_decorator(func, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            if self.__alive:
                ret = func(self, *args, **kwargs)
            else:
                msg = f"This experiment({self.__user_exp_id}) ended. Pleases initiate the new experiment."
                logger.log(logging.ERROR, msg=msg)
                raise TrumpetClientException(detail=msg)
            return ret
        return wrapper

    def set_hyperparam(self, hyper_parameter):
        if isinstance(hyper_parameter, dict):
            self.params["hyper_parameter"] = hyper_parameter
            self.artifact_management.send_parameter(file_type="hyper_parameter", hyper_map=self.params)
            return hyper_parameter
        else:
            detail = f"Please set dict Type data."
            raise TrumpetClientException(detail=detail)

    @alive_decorator
    def log(self, payload):
        if self.tracking_management.run_status is True:
            self.tracking_management.preparation_run()
        for key, value in payload.items():
            payload[key] = float(value)
        self.tracking_management.get_metrics(payload=payload)

    @alive_decorator
    def register_model(self,
                       model_name=None,
                       model_file_path=None,
                       description=None,
                       model_tag=None,
                       model_version=DEFAULT_MODEL_VERSION,
                       # artifact_set_id=None,
                       artifact_type_id="artifact_type_id",
                       parent_id=None,
                       is_registry="N",
                       ):
        return DealWithModel(
            user_id=self.__user_user_id,
            workspace_id=self.__user_workspace_id,
            project_id=self.__user_project_id,
            exp_id=self.__user_exp_id,
            team_id=self.__user_team_id,
            exp_name=self.__user_exp_name,
            model_name=model_name,
            file_path=model_file_path,
            description=description,
            model_tag=model_tag,
            artifact_set_id=self.artifact_set_id,
            artifact_type_id="model",
            model_version=model_version,
            auth=self.__api_keyInfo,
            parent_id=parent_id,
            is_registry=is_registry,
        ).requests_register_model()

    def register_datasets(self,
                          dataset_name=None,
                          dataset_file_path=None,
                          description=None):
        return self.artifact_management.send_datasets(file_name=dataset_name,
                                                      file_path=dataset_file_path,
                                                      file_type="datasets",
                                                      auth=self.__api_keyInfo
                                                      )

    @alive_decorator
    def handler_exit_time(self):
        start_time = self.start_time
        end_time = now()
        duration_time = (end_time - start_time).total_seconds()
        exp_info = experiment_init_info(start_time=start_time, end_time=end_time, duration_time=duration_time)
        self.artifact_management.send_artifact(file_type=SET_TYPE['experiment_info'], artifact_experiment=exp_info)
        self.artifact_management.inquiry_experiment(exp_id= self.__user_exp_id, auth=self.__api_keyInfo)
        # self.track_metric.delete_file()
        self.tracking_management.stop()

    @alive_decorator
    def stop(self):
        self.handler_exit_time()
        self.__alive = False

    # def __del__(self):
    #     logger.log(logging.INFO, msg = f"\nThe experiment({self.__user_exp_id}) ended successfully.\n")
