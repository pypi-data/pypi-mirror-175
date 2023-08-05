from trumpet_client.envs import *
from trumpet_client.api.crud import CRUD_API
from trumpet_client.launch.handler import installed_libray
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
from trumpet_client.envs import trumpetHeader
from trumpet_client.exceptions import *


# init function parameter api_key Exception
from trumpet_client.utils.datetime_utils import now, datetime_formatting


def _is_valid_user_api(api_key=None,
                       workspace_id=None,
                       project_id=None,
                       user_id=None,
                       exp_name=None,
                       tags=None,
                       description=None
                       ):
    init_api = CRUD_API(api_key=api_key)
    if not api_key or not workspace_id or not project_id or not user_id:
        if not api_key:
            raise TrumpetUnverfiedApiKey(api_key)
        elif not workspace_id:
            raise TrumpetUnverfiedWorkspaceId(workspace_id)
        elif not project_id:
            raise TrumpetUnverfiedProjectId(project_id)
        elif not user_id:
            raise TrumpetUnverfiedUserId(user_id)

    multipart_data = MultipartEncoder(
        fields={
            "userId": user_id,
            "apiKey": api_key,
            "workspaceId": workspace_id,
            "projectId": project_id,
            "expName": exp_name,
            "libFile": ("requirements.txt", f"{installed_libray}"),
            "tag": tags,
            "status": "T",
            "description": description,
            "startTime": datetime_formatting(now()),
            "createTime": datetime_formatting(now()),
            "updateTime": datetime_formatting(now())
        }
    )

    trumpetHeader["Content-Type"] = multipart_data.content_type

    check_api = init_api.init().create(
                              data=multipart_data,
                              headers=trumpetHeader
                              )

    try:
        if check_api['resCode'] == 200:
            print("Init Sucessfully!")
            return check_api
    except Exception:
        raise TrumpetServerErrorException()
