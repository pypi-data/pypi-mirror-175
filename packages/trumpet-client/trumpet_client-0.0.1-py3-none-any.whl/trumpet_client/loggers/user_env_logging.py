import os
import platform
import sys
import subprocess
import psutil
from trumpet_client.utils.datetime_utils import *
from trumpet_client.envs import *


def get_os_name():
    return platform.platform(aliased=True)


def get_os_type():
    return platform.system()


def get_python_version():
    return platform.python_version()


def get_work_path():
    return sys.argv[0]


def get_user_env():
    return {
        "os_name": get_os_name(),
        "os_type": get_os_type(),
        "python_version": get_python_version(),
        "run_path": get_work_path(),
        "host_name": platform.node(),
        "python_path": os.path.dirname(sys.executable),
        "trumpet_version": "0.0.2-dev",
        "cpu_count": psutil.cpu_count(),
        "memory_size": str(int(psutil.virtual_memory().total/1024**3)) + "GB"
    }


def experiment_init_info(start_time=None, end_time=None, duration_time=None):
    return {
        "start_datetime": now().date().isoformat(),
        "start_time": start_time.time().isoformat(),
        "end_time": end_time.time().isoformat(),
        "duration_time": str(duration_time)
    }


def get_conda_env_info():
    return subprocess.Popen(["conda env export"], shell=True, stdout=subprocess.PIPE).stdout.read().decode()
