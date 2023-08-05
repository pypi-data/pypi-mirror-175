import requests

DEFAULT_VERSION = "v1"
DEFAULT_HEADER = "api_key"

# TODO 삭제해야함
# DEFAULT_PROTOCOL = "http"
# DEFAULT_HOST = "localhost"
# DEFAULT_PORT = "19083"

DEFAULT_PROTOCOL = "https"
DEFAULT_HOST = "stag.trumpet.ai"
DEFAULT_PORT = "443"
DEFAULT_URL = f"{DEFAULT_PROTOCOL}://{DEFAULT_HOST}:{DEFAULT_PORT}/api"

URLS = {
    "v1":DEFAULT_URL,
    "v2":DEFAULT_URL,
    # "v1": "http://localhost:32089/api",
    # "v2": "http://localhost:32089/api",
}

END_POINTS = {
    "v1":{
        'user': '/user/',
        'team': '/core/team/',
        'workspace': '/core/workspace/',
        'project': '/core/project/',
        'experiments': '/core/exp/',
        'code': '/core/exp/ucode/',
        'model': '/core/model/',
        'model_registry': '/core/model-registry/',
        'artifact': '/core/artifact/',
        'artifact_set': '/core/artifact-set/',
        'init': '/core/init',
        'auth': '/user/login/apikey',
        's3': '/core/s3/download',
        'datasets': '/core/workspace/${id}/artifact?artifact_type_id={artifactType}'
    },
    "v2": {
        'user': '/user',
        'team': '/core/team',
        'workspace': '/core/workspace',
        'project': '/core/project',
        'experiments': '/core/exp',
        'code': '/core/exp/ucode',
        'model': '/core/model',
        'model_registry': '/core/model-registry/',
        'artifact': '/core/artifact',
        'artifact_set': '/core/artifact-set',
        'metric': '/core/metric',
        'init': '/auth/core/init',
        'project_model': '/core/project/{id}/model',
        'model_detail': '/core/model/{id}',
        'workspace_read': '/core/workspace/{id}/project',
        'auth': '/user/login/apikey',
        's3': '/core/s3/download',
        'datasets': '/core/workspace/{id}/artifact?artifact_type_id=datasets'
    },
}

METHOD_END_POINTS = {
    "v1":{
        "create": "add",
        "read": "read",
        "update": "edit",
        "delete": "del",
        "info": "info",

        "post": "add",
        "get": "read",
        "put": "edit",
    },
    "v2":{
        "create": "",
        "read": "/{id}",
        "update": "/{id}",
        "delete": "/{id}",
        "info": "/{id}",
        "post": "",
        "get": "/{id}",
        "put": "/{id}",
    }
}

METHOD_END_POINTS = {
    "v1":{
        "create": "add",
        "read": "read",
        "update": "edit",
        "delete": "del",
        "info": "info",

        "post": "add",
        "get": "read",
        "put": "edit",
    },
    "v2":{
        "create": "",
        "read": "/{id}",
        "update": "/{id}",
        "delete": "/{id}",
        "info": "/{id}",
        "post": "",
        "get": "/{id}",
        "put": "/{id}",
    }
}

METHODS = {
    "v1":{
        "create": requests.post,
        "read": requests.get,
        "update": requests.put,
        "delete": requests.delete,

        "post": requests.post,
        "get": requests.get,
        "info": requests.get,
        "put": requests.put,
    },
    "v2": {
        "create": requests.post,
        "read": requests.get,
        "update": requests.put,
        "delete": requests.delete,

        "post": requests.post,
        "get": requests.get,
        "info": requests.get,
        "put": requests.put,
    },
}