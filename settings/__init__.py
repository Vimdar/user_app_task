# pylint: skip-file
import os
from decouple import AutoConfig

config = AutoConfig(search_path=os.getcwd())
PRODUCTION = config('PRODUCTION', cast=bool)
from .common import *

if PRODUCTION:
    from .prod import *
else:
    from .dev import *
