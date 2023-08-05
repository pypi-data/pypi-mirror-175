import threading
import time
import psutil
import json as json_library
from trumpet_client.api import crud as CRUD_API
from trumpet_client.artifact.artifact_handler import artifact_start
from trumpet_client.utils.datetime_utils import *
import sys

import signal

# System Metrics Thread
class SystemMetric:
    def __init__(self, api_key, artifact_set_id=None):
        self.api = CRUD_API.CRUD_API(api_key=api_key)
        self.api_key = api_key
        self.artifact_id = artifact_start(api_key=api_key, artifact_type_id="system_metric", artifact_set_id=artifact_set_id)
        self.event = threading.Event()
        self.network_send = psutil.net_io_counters().bytes_sent
        self.network_recv = psutil.net_io_counters().bytes_recv
        self.system_metric = threading.Thread(target=self.get_system_metrics, daemon=True)
        self.interval_time = 10
        self.jupyter_stop = False
        self.thread_id = threading.get_ident()
        # while True:
        #     print("Thread keep check, ", self.system_metric.is_alive())
        #     time.sleep(5)

    def _signal_handler(self, signo, frames):
        sys.exit(0)

    def start(self):
        self.system_metric.start()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)



    def stop(self):
        self.event.set()
        self.system_metric.join()

    def _jupyter_stop(self):
        self.jupyter_stop = True
        self.event.set()
        self.system_metric.join()

    def is_alive(self):
        return self.system_metric.is_alive()

    def total_system_mean(self, payload):
        cpu_info = sum([info_cpu['cpu'] for info_cpu in json_library.loads(payload)])/len(json_library.loads(payload))
        mem_info = sum([info_memory['memory'] for info_memory in json_library.loads(payload)])/len(json_library.loads(payload))
        disk_info = sum([infocpu['disk'] for infocpu in json_library.loads(payload)])/len(json_library.loads(payload))
        net_info_send = sum([info_net['network_status']['send'] for info_net in json_library.loads(payload)])/len(json_library.loads(payload))
        net_info_recv = sum([info_net['network_status']['recv'] for info_net in json_library.loads(payload)])/len(json_library.loads(payload))
        system_metric = {
            "Cpu": round(cpu_info, 2),
            "Memory": round(mem_info, 2),
            "Disk": round(disk_info, 2),
            "Network Send": round(net_info_send, 2),
            "Network Receive": round(net_info_recv, 2),
            "create_time": now()
        }
        return system_metric

    def get_system_metrics(self):
        while not self.event.is_set():
            payload = {
                "metric": json_library.dumps(self.total_system_mean(json_library.dumps(self.user_system_status())), default=str)
            }
            self.send_metrics(payload)
            # print("payload: ", payload)
            # if self.jupyter_stop:
            #     break

    def is_main_thread(self):
        try:
            back_up = signal.signal(signal.SIGINT, signal.SIG_DFL)
        except ValueError:
            return False
        signal.signal(signal.SIGINT, back_up)
        return True

    def system_infos(self):
        status = {}
        network = psutil.net_io_counters()
        status["cpu"] = psutil.cpu_percent()
        status["memory"] = psutil.virtual_memory().percent
        status["disk"] = psutil.disk_usage("/").percent
        status["network_status"] = {
            "send": network.bytes_sent - self.network_send,
            "recv": network.bytes_recv - self.network_recv
        }

        return status

    def user_system_status(self):
        artifact_metric_get = []
        metic_timeout = time.time() + self.interval_time
        while True:
            if time.time() > metic_timeout:
                break
            artifact_metric_get.append(self.system_infos())
            time.sleep(2)
        return artifact_metric_get

    def send_metrics(self, payload):
        headers = {"api_key": self.api_key}
        params = {"id": self.artifact_id}
        result = self.api.metric().update(headers=headers, params=params, json=payload)
        return result

    def delete_file(self):
        headers = {"api_key": self.api_key}
        params = {"id": self.artifact_id}
        api = CRUD_API.CRUD_API.metric().delete(headers=headers, params=params)