from datetime import datetime
from trumpet_client.envs import DATETIME_FORMAT

now = datetime.now
datetime_formatting = lambda time: datetime.strftime(time, DATETIME_FORMAT)
