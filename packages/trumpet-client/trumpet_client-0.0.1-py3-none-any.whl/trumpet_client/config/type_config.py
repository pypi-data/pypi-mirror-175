from trumpet_client.exceptions import TrumpetMetricTypeException


def metrics_type_check(obj, type):
    if isinstance(obj, type):
        return True
    else:
        raise TrumpetMetricTypeException

