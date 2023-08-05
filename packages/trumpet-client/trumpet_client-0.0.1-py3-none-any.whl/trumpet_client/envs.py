ERROR_STYLE = {
    "h1": "",
    "h2": "",
    "end": "",
}

dev_version = "0.0.1"

# test init post url 1. (yoonDevServer) 2. (company server) 4.(port
# initUrl = "http://192.168.0.94:9081/api/core/init"
# initUrl = "http://192.168.0.174:19081/api/core/init"
# initUrl = "http://192.168.0.174:8080/api/core/init"
# initUrl = "http://192.168.0.174:32081/api/core/init"
#
# test metrices post url 1. (yoonDevServer) 2. (company server)
# metricesUrl = "http://192.168.0.94:9081/api/core/exp/metric"
# metricesUrl = "http://192.168.0.174:19081/api/core/exp/metric"
metricesUrl = "http://192.168.0.174:8080/api/core/exp/metric"


# test register model server 1. (yoonDevServer), 2. (companyServer)
# registerModelUrl = "http://192.168.0.94:9081/api/core/model/add"
# registerModelUrl = "http://192.168.0.174:32081/api/core/model/add"
# registerModelUrl = "http://192.168.0.174:8080/api/core/model/add"


# test source Code send url 1. (yoonDevServer) 2. (company server 32081)
# sendUserUrl = "http://192.168.0.94:9081/api/core/exp/ucode"
# sendUserUrl = "http://192.168.0.174:19081/api/core/exp/ucode"
# sendUserUrl = "http://192.168.0.174:8080/api/core/exp/ucode"
# sendUserUrl = "http://192.168.0.174:32081/api/core/exp/ucode"

# apikey TODO 제거
apikey = "7e5b91e535c8e8fda2614420a4c1e5ff4e67438e455119c77b6ba65c027948d1"

# test header information
trumpetHeader = {"x-api-key": apikey}


# test header register model
registerModelHeader = {"x-api-key": apikey}

DEV_API_MAPPING = {
    "Integrated_init_url": {
        "url": "http://localhost:19081/api/core/init",
        "header": {"x-api-key": apikey}
    },
}
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"