import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
from trumpet_client.envs import trumpetHeader, DEV_API_MAPPING
from trumpet_client.launch.handler import _get_file_path
from trumpet_client.envs import *

# 추후 제거
class ManagementSourceCode:
    def __init__(self, start_time, end_time, duration_time, exp_id, project_id, exp_name):
        self.start_time = start_time
        self.end_time = end_time
        self.duration_time = duration_time
        self.exp_id = exp_id
        self.project_id = project_id
        self.exp_name = exp_name

    def send_source_code(self):
        multipart_data = MultipartEncoder(
            fields={
                "expId": self.exp_id,
                "expName": self.exp_name,
                "prtId": self.project_id,
                "status": "sdsads",
                "tag": "sdsd13",
                "startTime": datetime.strftime(self.start_time, DATETIME_FORMAT),
                "endTime": datetime.strftime(self.end_time, DATETIME_FORMAT),
                "file": (os.path.basename(_get_file_path()), open(_get_file_path(), "rb")),
                "durationTime": self.duration_time
            }
        )
        trumpetHeader["Content-Type"] = multipart_data.content_type

        res = requests.post(url=DEV_API_MAPPING['Integrated_send_url']['url'],
                            data=multipart_data,
                            headers=trumpetHeader
                            )
        print("상태 정보: ", res.content.decode("utf-8"))
