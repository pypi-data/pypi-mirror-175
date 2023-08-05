import platform
from trumpet_client.launch.new_init import Init
from trumpet_client.launch.init_model import InitModel
from trumpet_client.launch.init_datasets import InitDatasets
from trumpet_client.envs import dev_version
init = Init
init_model = InitModel
init_datasets = InitDatasets


# trumpet ai version check
def version():
    """
    :return:  trumpet.ai version
    """
    return dev_version


def platformCheck():
    print("your system platform: ", platform.platform())
