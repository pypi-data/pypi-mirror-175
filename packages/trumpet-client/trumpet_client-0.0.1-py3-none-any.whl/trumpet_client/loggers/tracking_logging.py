import logging
import json as json_library
from trumpet_client.artifact.artifact_handler import artifact_start
from trumpet_client.api import crud as CRUD_API
from trumpet_client.utils.datetime_utils import *
from trumpet_client.loggers.system_logging import SystemMetric
from typing import Dict, Union


class TrackingManagement:
    def __init__(self, api_key, artifact_setup):
        self.api_key = api_key
        self.artifact_setup = artifact_setup
        self.run_status = True
        self.tracking = None

     # 한번 호출
    def trackingMetrics(self):
        return TrackingMetrics(api_key=self.api_key, artifact_setup=self.artifact_setup)

     # 한번 호출  run 메서드 호출시
    def preparation_run(self):
        if self.run_status:
            self.run_status = False
            self.tracking = self.trackingMetrics()

    def get_metrics(self, payload):
        return self.tracking.get_payload_values(payload=payload)

    def stop(self):
        if self.run_status is not False:
            return None
        return self.tracking.delete_file()


class TrackingMetrics:
    def __init__(self, api_key=None, artifact_setup=None):
        self.artifact_setup = artifact_setup
        self.api_key = api_key
        self.api = CRUD_API.CRUD_API(api_key=api_key)
        self.artifact_id = artifact_start(api_key=api_key, artifact_name="experiment_metrics", artifact_type_id="learning_metric", artifact_set_id=self.artifact_setup['artifactSetId'])
        self.initial_checker = False
        self.stop_cker = False
        self.payload = []

    def get_payload_values(self, payload):
        if not self.initial_checker:
            self.initial_checker = True
            self.system_metric = SystemMetric(api_key=self.api_key, artifact_set_id=self.artifact_setup['artifactSetId'])
            msg = f"Start collecting system metric data. {self.system_metric.is_alive()}"
            logging.info(msg=msg)
            self.system_metric.start()
        self.payload.append(payload)
        self.experiment_metrics_update(payload=payload)

    def experiment_metrics_update(self, payload):
        payload['create_time'] = now()
        ## thrading start
        user_payload = {
            "metric": json_library.dumps(payload, default=str),
        }
        params = {"id": self.artifact_id}
        result = self.api.metric().update(params=params, json=user_payload)
        return result

    def delete_file(self):
        self.stop_cker = True
        headers = {"api_key": self.api_key}
        params = {"id": self.artifact_id}
        api = CRUD_API.CRUD_API.metric().delete(headers=headers, params=params)

        if self.stop_cker:
            self.system_metric.stop()
            self.system_metric.delete_file()
