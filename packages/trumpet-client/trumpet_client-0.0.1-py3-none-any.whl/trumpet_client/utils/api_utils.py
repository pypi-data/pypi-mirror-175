from trumpet_client.config.api_config import *
from typing import Union


def get_url(version: str=DEFAULT_VERSION, ) -> str:
    return URLS[version]

def get_end_point(end_point: str, version: str=DEFAULT_VERSION,) -> str:
    return END_POINTS[version][end_point]

def get_method(method_name: str, version: str=DEFAULT_VERSION,) -> requests.request:
    return METHODS[version][method_name]

def get_method_end_point(method_name: str, version: str=DEFAULT_VERSION,) -> object:
    return METHOD_END_POINTS[version][method_name]

def get_full_url(url: str, end_point: str, params: dict, method_end_point: str = None):
    full_url = f"{url}{end_point}{method_end_point}"
    for k, v in params.items():
        full_url = full_url.replace(f"{{{k}}}",v)
    return full_url

def get_request(url: str, end_point: str, json: object, headers: dict, method_name: str, params: dict, version: str=DEFAULT_VERSION, data=None, files=None) -> requests.Response:
    json = {"reqDetail": json}


    method_end_point = get_method_end_point(method_name, version=version)

    full_url = get_full_url(url, end_point, params=params, method_end_point=method_end_point)
    method = get_method(method_name, version=version)
    response = method(url=full_url, json=json, headers=headers, data=data, files=files)

    return response

# 32081 -------> 32089 변경 필요
def browse_param_requests(url: str, end_point: str, id: str, json: dict, auth: Union[str, dict], artifact_type: str = None):
    # if isinstance(auth, dict) and artifact_type is None:
    #     res = requests.get(url=f"http://localhost:32081/api"+end_point.replace('{id}', id), headers={"Authorization": auth["Authorization"]["Authorization"]})
    # elif artifact_type == "datasets" or artifact_type == "model":
    #     artifact_json = {"reqDetail": json}
    #     res = requests.get(url=f"http://localhost:32081/api"+end_point, json=artifact_json, headers={"Authorization": auth})
    # else:
    #     res = requests.get(url=f"http://localhost:32081/api"+end_point.replace('{id}', id), headers={"Authorization": auth})
    # return res

    if isinstance(auth, dict) and artifact_type is None:
        res = requests.get(url=f"{url}"+end_point.replace('{id}', id), headers={"Authorization": auth["Authorization"]["Authorization"]})
    elif artifact_type == "datasets" or artifact_type == "model":
        artifact_json = {"reqDetail": json}
        res = requests.get(url=f"{url}"+end_point, json=artifact_json, headers={"Authorization": auth})
    else:
        res = requests.get(url=f"{url}"+end_point.replace('{id}', id), headers={"Authorization": auth})
    return res


def camel_to_snake(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('__([A-Z])', r'_\1', string)
    string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    return string.lower()


def snake_to_camel(string):
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


# def type_checker(obj, type) -> None:
#     if isinstance(obj, type):
#         pass
#     else:
#         raise TypeError("Type Eroor")
