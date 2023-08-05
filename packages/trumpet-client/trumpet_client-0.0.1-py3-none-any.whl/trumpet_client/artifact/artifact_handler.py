from trumpet_client.api.api_var import snake_to_camel
from trumpet_client.launch.handler import _get_file_path
from trumpet_client.launch.handler import installed_libray
from trumpet_client.loggers.user_env_logging import (get_user_env, get_conda_env_info)
from trumpet_client.envs import *
from trumpet_client.api import crud as CRUD_API
import os
from datetime import datetime


def artifact_start(api_key=None, artifact_name=None, artifact_type_id=None, artifact_set_id=None):
    headers = {"api_key": api_key}
    artifact_form = {
        "artifact_name": artifact_name,
        "create_time": datetime.now().strftime(DATETIME_FORMAT),
        "update_time": datetime.now().strftime(DATETIME_FORMAT),

        "create_user_id": "admin", #TODO 영남님이 바꿈
        "update_user_id": "",
        "description": "",
        "version": "",
        "tag": "",
        "artifact_set_id": artifact_set_id,
        "artifact_type_id": artifact_type_id
    }
    # snake to camel
    artifact_form = {snake_to_camel(key):val for key, val in artifact_form.items()}
    crud_api = CRUD_API.CRUD_API(api_key=api_key).metric().create(headers=headers, data=artifact_form)

    return crud_api['resResult']['artifactId']


def artifact_setup(api_key=None, workspace_id=None, project_id=None, exp_id=None, team_id=None):
    headers = {"api_key": api_key}
    artifact_form = {
        "team_id": team_id,
        "work_id": workspace_id,
        "prt_id": project_id,
        "exp_id": exp_id,
        "tag": []
    }
    artifact_crud_api = CRUD_API.CRUD_API(api_key=api_key).artifact_set().create(headers=headers, json=artifact_form)
    return artifact_crud_api['resResult']


def separate_file_type(create_user_id=None, artifact_name=None, artifact_set_id=None, file_type=None, artifact_experiment=None, description=None):
    artifact_form = {
        "createUserId": create_user_id,
        "artifactName": artifact_name,
        "artifactSetId": artifact_set_id,
        "description": description,
    }
    files = ''
    if _get_file_path() is not None:
        if file_type == "source_code":
            artifact_form["artifactTypeId"] = "source_code"
            files = [
                ("file", (os.path.basename(_get_file_path()), open(_get_file_path(), "rb")))
            ]

    if file_type == "requirements":
        artifact_form["artifactTypeId"] = "package_list"
        files = [
            ("file", ("requirements.txt", f"{installed_libray}"))
        ]
    if file_type == "user_os_info":
        artifact_form["artifactTypeId"] = "user_os_info"
        files = [
            ("file", ("user_os_info.json", f"{get_user_env()}"))
        ]
    if file_type == "conda_environment":
        artifact_form["artifactTypeId"] = "conda_environment"
        files = [
            ("file", ("conda_environment.yaml", f"{get_conda_env_info()}"))
        ]
    if file_type == "experiment_info":
        artifact_form["artifactTypeId"] = "experiment_info"
        files = [
            ("file", ("info_experiment.json", f"{artifact_experiment}"))
        ]
    return artifact_form, files


def process_hyperparameter(artifact_name=None, artifact_set_id=None, file_type=None, hyper_map=None):
    artifact_form = {
        "artifactName": artifact_name,
        "artifactSetId": artifact_set_id,
        "artifactTypeId": file_type,
    }
    files = [("file", ("hyperparameter_info.txt", f"{str(hyper_map)}"))]
    return artifact_form, files


def process_datasets(artifact_name=None, artifact_set_id=None, file_type=None, file_name=None, file_path=None):
    artifact_form = {
        "artifactName": artifact_name,
        "artifactSetId": artifact_set_id,
        "artifactTypeId": file_type,
    }
    files = [
        ("file", (file_name+".csv", open(file_path, "rb")))
    ]

    return artifact_form, files
