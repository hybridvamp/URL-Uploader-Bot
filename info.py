import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

AUTH_CHANNEL = os.environ[AUTH_CHANNEL]
