import sys
import os.path
import re
import ipykernel
import requests
import pkg_resources
import json
import IPython
from notebook.notebookapp import list_running_servers
from urllib.parse import urljoin
from trumpet_client.exceptions import TrumpetJupyterFileTimeout

# get user python environment requirements.txt
installed_libray = "\n".join([i.key for i in pkg_resources.working_set])


def _get_user_notebook_name():
    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'), params={'token': ss.get('token', '')}, timeout=5)
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)


def _user_jupyter_environment():
    user_ipy = IPython.get_ipython()
    if hasattr(user_ipy, "kernel"):
        return True
    else:
        return False


def _check_user_environment():
    if _user_jupyter_environment():
        try:
            ##TODO ipynb 기능 보류
            # user_file_name = _get_user_notebook_name()
            # return user_file_name
            return None
        except Exception:
            raise TrumpetJupyterFileTimeout()

    else:
        return sys.argv[0]


def _get_file_path():

    ##TODO ipynb 기능 보류
    file_name = _check_user_environment()

    if file_name is None:
        return None

    if file_name.split(".")[-1] == "ipynb" or file_name.split(".")[-1] == "py":
        return file_name